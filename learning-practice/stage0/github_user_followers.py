import json
import sys
import urllib.request


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def fetch_github_user(username):
    url = f"https://api.github.com/users/{username}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "stage0-learning-practice",
        },
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    user = fetch_github_user("torvalds")
    print("login:", user["login"])
    print("name:", user["name"])
    print("followers:", user["followers"])


if __name__ == "__main__":
    main()
