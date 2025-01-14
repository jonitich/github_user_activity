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

def get_repo_commits(repo, user):
    """ Get all commits """
    
    activity = fetch_activity(user)
    i = 0
    for event in activity:
        if event["repo"]["name"] == repo and event["type"] == "PushEvent" and event["payload"]["commits"]:
            i += 1
    return i

def get_repo_names(user):
    """ Get all repos' name fetched and delete duplications. """
    
    activity = fetch_activity(user)
    repos = {repo["repo"]["name"] for repo in activity}
    return repos

def main():
    # User Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("user", type=str, help="User to get activity from.")
    parser.add_argument("--debug", help="Print all events")
    
    # Parse argument
    args = parser.parse_args()
    print(args)
    
    # Get activity
    activity = fetch_activity(args.user)
    if args.debug:
        for event in activity:
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(event)
            print("----------------------------------------------------")
    for event in activity: # Print events other than PushEvent
        repo = event["repo"]["name"]
        if event["type"] == "IssuesEvent":
            print(f"- Opened a Issue in {repo}.")
        elif event["type"] == "WatchEvent":
            print(f"- Starred {repo}.")
    
    for repo in get_repo_names(args.user): # Print PushEvent
        commits = get_repo_commits(repo, args.user)
        if not commits == 0:
            print(f"- Pushed {commits} to {repo}.")


if __name__ == "__main__":
    main()


# if event["type"] == "PushEvent":
#     commits = get_repo_commits(event["repo"]["name"], args.user)
#     if not commits == 0:
#         print(f"- Pushed {commits} commits to {repo}")