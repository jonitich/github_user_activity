import requests
import argparse
import os

# Constant values
api = "https://api.github.com/"
token_path = os.getenv("FILE_PATH")

def auth():
    with open(token_path, "r") as f:
        token = f.read().strip()
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

def get_events(repo, event_type, activity):
    """ Get events """
    
    i = 0
    for event in activity:
        if event["repo"]["name"] == repo and event["type"] == event_type:
            i += 1
    return i


def get_repo_names(events):
    """ Get all repos' name and event type fetched and delete duplications. """
    
    repos = {repo["repo"]["name"] for repo in events}
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
        
        for repo in get_repo_names(activity): # Print PushEvent
            commits = get_events(repo, "PushEvent", activity)
            issues_events = get_events(repo, "IssuesEvent", activity)
            watch_events = get_events(repo, "WatchEvent", activity)
            if watch_events > 0:
                watch_events = True
            else:
                watch_events = False
            pr_events= get_events(repo, "PullRequestEvent", activity)
            print(f"Events on repository: {repo}\n \
                    - Commits: {commits} \n \
                    - Opened Issues: {issues_events} \n \
                    - Starred: {watch_events} \n \
                    - Pull Requests: {pr_events}")



if __name__ == "__main__":  
    main()
