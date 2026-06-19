import json
import os
import sys
import urllib.error
import urllib.request


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


API_URL = "https://api.github.com/user"


def call_github_user(token=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "stage0-api-auth-practice",
        "X-GitHub-Api-Version": "2026-03-10",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(API_URL, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8")
        return error.code, json.loads(body)


def print_result(title, status_code, data):
    print(title)
    print("  status:", status_code)
    if "login" in data:
        print("  login:", data["login"])
        print("  name:", data.get("name"))
    else:
        print("  message:", data.get("message"))


def main():
    status_code, data = call_github_user()
    print_result("Without token:", status_code, data)

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print()
        print("GITHUB_TOKEN is not set yet.")
        print("Set it first, then run this script again.")
        return

    print()
    status_code, data = call_github_user(token)
    print_result("With token:", status_code, data)


if __name__ == "__main__":
    main()
