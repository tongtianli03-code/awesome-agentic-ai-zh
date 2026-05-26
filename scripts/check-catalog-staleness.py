#!/usr/bin/env python3
"""
check-catalog-staleness.py — flag catalog entries pointing to dormant or archived repos.

`refresh-stars.py` (weekly) keeps star counts current but doesn't tell you which
repos are zombie listings — projects that haven't shipped in a year, or were
quietly archived. This script reads every GitHub URL in the corpus, queries
`gh api repos/<owner>/<repo>` for `pushed_at` + `archived`, and reports entries
whose most recent push is older than the threshold (default 12 months) or whose
repo is archived.

**Report-only**. Does NOT modify markdown. Mirrors weekly-catalog-refresh's
broken-link policy: open an issue, let the maintainer decide what to do per
entry (annotate with ⚠ note / move to "historical reference" / drop).

Usage:
    python scripts/check-catalog-staleness.py                     # default: >=12 months
    python scripts/check-catalog-staleness.py --months 18         # bump threshold
    python scripts/check-catalog-staleness.py --format markdown   # GH issue body
    python scripts/check-catalog-staleness.py --format json       # CI ingestion
    python scripts/check-catalog-staleness.py --check             # exit 1 if any stale

Env:
    `gh` (GitHub CLI) on PATH, authenticated.

Exit codes:
    0 — no stale repos (or default report mode finished)
    1 — `--check` mode and stale repos found
    2 — environment error (gh missing / auth failed)
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MD_GLOB = "**/*.md"
EXCLUDE_DIRS = {".git", ".ai", "node_modules", "_build", ".venv", "_archive"}

GITHUB_RE = re.compile(r"https://github\.com/([\w.-]+)/([\w.-]+?)(?:[#?/)\s]|$)")

# Mirror refresh-stars.py exclusion lists (kept in sync deliberately — these
# are not "repos" in the GitHub sense).
PLACEHOLDER_REPOS = {
    "owner/repo", "example/repo", "your-org/your-repo", "user/repo",
}
NON_REPO_OWNERS = {
    "settings", "marketplace", "login", "logout", "join",
    "topics", "trending", "collections", "events", "explore",
    "issues", "pulls", "notifications", "search", "new",
    "organizations", "users", "blog", "about", "pricing",
    "features", "security", "enterprise", "customer-stories",
}

MAX_WORKERS = 10


def normalize_repo(owner: str, name: str) -> str | None:
    """Drop placeholder + non-repo paths. Mirrors refresh-stars.py."""
    name = name.removesuffix(".git")
    repo_id = f"{owner}/{name}"
    if repo_id in PLACEHOLDER_REPOS:
        return None
    if owner in NON_REPO_OWNERS:
        return None
    if len(owner) < 1 or len(name) < 1:
        return None
    return repo_id


def find_md_files(root: Path) -> list[Path]:
    files = []
    for fp in root.glob(MD_GLOB):
        if any(part in EXCLUDE_DIRS for part in fp.parts):
            continue
        files.append(fp)
    return files


def find_github_repos(root: Path) -> dict[str, list[tuple[Path, int]]]:
    """Scan all .md files; return {repo_id: [(file, line_no), ...]}."""
    entries: dict[str, list[tuple[Path, int]]] = {}
    for fp in find_md_files(root):
        try:
            lines = fp.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(lines, start=1):
            for m in GITHUB_RE.finditer(line):
                repo = normalize_repo(m.group(1), m.group(2))
                if repo is None:
                    continue
                entries.setdefault(repo, []).append((fp, i))
    return entries


def fetch_repo_meta(repo: str) -> dict | None:
    """Query gh api for pushed_at, archived, stargazers_count.

    Returns None if the API call fails (404 / private / renamed / rate-limit).
    """
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{repo}",
             "--jq", "{pushed_at, archived, stargazers_count}"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout.strip())
        return data
    except (subprocess.SubprocessError, json.JSONDecodeError, ValueError):
        return None


def parse_pushed_at(s: str | None) -> datetime | None:
    """`2024-08-26T14:32:11Z` -> datetime."""
    if not s:
        return None
    try:
        # GH returns ISO 8601 with trailing Z; Python <3.11 needs explicit handling
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def months_ago(dt: datetime, now: datetime) -> float:
    """Calendar-month-ish diff. Good enough for thresholding."""
    return (now - dt).days / 30.44  # avg days per month


def main():
    # Windows defaults to cp950/cp1252; this script prints em-dash + ⚠️ +
    # other non-ASCII (esp. in --format markdown / json). Force UTF-8 stdout.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--months", type=int, default=12,
                        help="Threshold in months (default: 12). Repos with pushed_at older "
                             "than this are flagged.")
    parser.add_argument("--format", choices=["text", "markdown", "json"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--check", action="store_true",
                        help="Exit 1 if any stale repos found (for CI gating)")
    parser.add_argument("--include-archived-only", action="store_true",
                        help="Skip pushed_at threshold; report ONLY archived repos")
    args = parser.parse_args()

    # Sanity-check gh on PATH (don't waste time finding URLs if auth is busted)
    probe = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
    if probe.returncode != 0:
        print("error: `gh` CLI not authenticated. Run `gh auth login` first.",
              file=sys.stderr)
        sys.exit(2)

    entries = find_github_repos(REPO_ROOT)
    unique_repos = sorted(entries.keys())
    print(f"Found {len(unique_repos)} unique GitHub repos in catalog.",
          file=sys.stderr)
    print(f"Querying gh api for pushed_at / archived...", file=sys.stderr)

    # Parallel fetch
    meta: dict[str, dict | None] = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(fetch_repo_meta, r): r for r in unique_repos}
        for i, fut in enumerate(as_completed(futures), start=1):
            repo = futures[fut]
            meta[repo] = fut.result()
            if i % 20 == 0:
                print(f"  {i}/{len(unique_repos)}", file=sys.stderr)

    now = datetime.now(timezone.utc)
    stale = []  # list of dict: {repo, occurrences, pushed_at, months, archived, stars}
    not_found = []

    for repo in unique_repos:
        m = meta[repo]
        if m is None:
            not_found.append(repo)
            continue
        archived = bool(m.get("archived"))
        pushed = parse_pushed_at(m.get("pushed_at"))
        stars = m.get("stargazers_count")

        if args.include_archived_only:
            is_stale = archived
        else:
            months = months_ago(pushed, now) if pushed else None
            is_stale = archived or (months is not None and months >= args.months)

        if not is_stale:
            continue

        stale.append({
            "repo": repo,
            "occurrences": [(fp.relative_to(REPO_ROOT).as_posix(), ln)
                            for fp, ln in entries[repo]],
            "pushed_at": pushed.date().isoformat() if pushed else None,
            "months_since_push": round(months_ago(pushed, now), 1) if pushed else None,
            "archived": archived,
            "stars": stars,
        })

    # Sort: archived first, then by months_since_push desc
    stale.sort(key=lambda x: (not x["archived"],
                              -(x["months_since_push"] or 0)))

    if args.format == "json":
        json.dump({
            "threshold_months": args.months,
            "checked_at": now.isoformat(),
            "total_repos": len(unique_repos),
            "stale_count": len(stale),
            "not_found_count": len(not_found),
            "stale": stale,
            "not_found": not_found,
        }, sys.stdout, indent=2)
        print()
    elif args.format == "markdown":
        _emit_markdown(stale, not_found, args.months, now, len(unique_repos))
    else:
        _emit_text(stale, not_found, args.months, len(unique_repos))

    if args.check and (stale or not_found):
        sys.exit(1)


def _emit_text(stale, not_found, months, total):
    print()
    print("=" * 68)
    print(f"Total repos checked:    {total - len(not_found)}")
    print(f"Stale (>= {months} months OR archived):  {len(stale)}")
    print(f"Not found (404 / private):  {len(not_found)}")
    print()

    if stale:
        print("=== Stale catalog entries ===")
        for s in stale:
            flag = "ARCHIVED" if s["archived"] else f"{s['months_since_push']}mo"
            stars = f"  ★{s['stars']}" if s['stars'] is not None else ""
            print(f"  [{flag:>9}]  {s['repo']}{stars}  last push {s['pushed_at']}")
            for path, line in s["occurrences"][:3]:
                print(f"             -> {path}:{line}")
            if len(s["occurrences"]) > 3:
                print(f"             -> ... +{len(s['occurrences']) - 3} more")

    if not_found:
        print()
        print("=== Repos not found (404 / private / renamed) ===")
        for repo in not_found:
            print(f"  {repo}")


def _emit_markdown(stale, not_found, months, now, total):
    """Markdown body suitable for `gh issue create --body-file -`."""
    print(f"# Catalog staleness report — {now.date().isoformat()}\n")
    print(f"Threshold: **{months} months** since last push, or `archived: true`.")
    print(f"Total repos in catalog: **{total}**. "
          f"Stale: **{len(stale)}**. Not found: **{len(not_found)}**.\n")

    if stale:
        print("## Stale entries\n")
        print("| Repo | Flag | Last push | Stars | Locations |")
        print("|---|---|---|---|---|")
        for s in stale:
            flag = "⚠️ archived" if s["archived"] else f"⏰ {s['months_since_push']}mo"
            stars = s["stars"] if s["stars"] is not None else "—"
            locs = "<br>".join(f"`{p}:{ln}`" for p, ln in s["occurrences"][:5])
            if len(s["occurrences"]) > 5:
                locs += f"<br>… +{len(s['occurrences']) - 5} more"
            print(f"| [{s['repo']}](https://github.com/{s['repo']}) | {flag} | "
                  f"{s['pushed_at']} | {stars} | {locs} |")

    if not_found:
        print("\n## Not found (404 / private / renamed)\n")
        for repo in not_found:
            print(f"- `{repo}`")

    print("\n## Suggested actions per entry\n")
    print("1. **Archived but still teaches something** — keep listed, add `⚠️ Archived (YYYY-MM)` to the entry's Notes column.")
    print("2. **Dormant, but project alive elsewhere (fork / rename)** — update URL, optionally note original.")
    print("3. **Dormant and superseded** — replace with the maintained alternative; drop or keep as 'historical reference'.")
    print("4. **Dormant but uniquely valuable (no alternative)** — keep, no annotation needed.")
    print("\n*Generated by `scripts/check-catalog-staleness.py` — re-run after triage to confirm a clean report.*")


if __name__ == "__main__":
    main()
