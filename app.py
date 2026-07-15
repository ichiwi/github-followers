import requests
import os
import time

USERNAME = "ENTER_YOUR_GITHUB_USERNAME_HERE" # Update this

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
}

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

def fetch_all(url):
    results = []
    while url:
        response = requests.get(url, headers=HEADERS, timeout=20)
        if response.status_code != 200:
            print(f"Failed to fetch: {url} ({response.status_code})")
            break
        results.extend(response.json())
        url = response.links.get("next", {}).get("url")
    return results

def main():
    followers_url = f"https://api.github.com/users/{USERNAME}/followers"
    following_url = f"https://api.github.com/users/{USERNAME}/following"

    followers = {user["login"] for user in fetch_all(followers_url)}
    following = {user["login"] for user in fetch_all(following_url)}

    accounts_not_following_back = following - followers
    accounts_not_followed_back = followers - following

    if accounts_not_following_back == set():
        print("\nYou are following everyone who is following you.")
    else:
        print("\nUsernames of those you're following, but they're not following you back:")
        print(accounts_not_following_back)

    if accounts_not_followed_back == set():
        print("\nYou are followed by everyone you are following.")
    else:
        print("\nUsernames of those following you, but you're not following back:")
        print(accounts_not_followed_back)

if __name__ == "__main__":
    main()
