import requests
import json
import argparse
import io

def read_token():
    file = io.open("/home/jredondo/programming/.github/github_user_activity.token", "r")
    token = file.readline().strip('\n')
    file.close()
    return token

def fetch_activity(user):
    """ Get github's user actitvity """
    
    headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer " + str(read_token()),
    "X-GitHub-Api-Version": "2022-11-28"
    }
    req = requests.get(f"https://api.github.com/users/{user}/events/public", headers=headers)
    return req.json()

def get_event_from_repo(repo, user):
    """ Get all events of a repo """
    
    print(f"Checking events of {repo} repository.")
    activity = fetch_activity(user)
    
    # Commit loop
    i = 0
    for event in activity:
        if event["repo"]["name"] == repo and event["type"] == "PushEvent" and event["payload"]["commits"]:
            i += 1
    
    print(f"- Pushed {i} commits to {repo}")

def get_repo_names(user):
    """ Group repos' names """
    
    activity = fetch_activity(user)
    repos = {repo["repo"]["name"] for repo in activity}
    return repos


def main():
    # User Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("user", type=str, help="User to get activity from.")
    
    # Parse argument
    args = parser.parse_args()
    
    # Get activity
    repos = get_repo_names(args.user)
    for repo in repos:
        get_event_from_repo(repo, args.user)


if __name__ == "__main__":
    main()