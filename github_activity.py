import requests
import json
import argparse
import io

# Constant values
api = "https://api.github.com/"

def auth():
    file = io.open("/home/jredondo/programming/.github/github_user_activity.token", "r")
    token = file.readline().strip('\n')
    file.close()
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + str(token),
        "X-GitHub-Api-Version": "2022-11-28"
    }
    return headers

def verify_user(user):
    """ Verify if the user exists """
    
    req = requests.get(f"{api}/users/{user}")
    if req.status_code == 200:
        return True
    else:
        return False

def fetch_activity(user):
    """ Get github's user actitvity """
    
    req = requests.get(f"{api}users/{user}/events/public", headers=auth())
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
    
    # Verify User
    user = verify_user(args.user)
    if not user:
        print(f"There's no such user {args.user}")
    else:
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
