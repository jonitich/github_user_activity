import requests
import argparse
import os

# Constant values
api = "https://api.github.com/"
token = os.getenv("GITHUB_TOKEN", "error")
if token == "error":
    raise Exception("Set GITHUB_TOKEN environment variable.")


def auth():
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + str(token),
        "X-GitHub-Api-Version": "2022-11-28",
    }
    return headers


def verify_user(user):
    """Verify if the user exists"""

    req = requests.get(f"{api}/users/{user}")
    if req.status_code == 200:
        return True
    else:
        return False


def fetch_activity(user):
    """Get github's user actitvity"""

    req = requests.get(f"{api}users/{user}/events/public", headers=auth())
    if req.status_code != 200:
        print(f"Error fetching activity: {req.status_code}")
        return []
    return req.json()


def preprocess_events(activity):
    """
    Preprocess activity data to categorize events by repository and event type.
    This reduces redundant iterations during analysis.
    """
    processed_data = {}
    for event in activity:
        repo_name = event["repo"]["name"]
        event_type = event["type"]
        if repo_name not in processed_data:
            processed_data[repo_name] = {}
        if event_type not in processed_data[repo_name]:
            processed_data[repo_name][event_type] = 0
        processed_data[repo_name][event_type] += 1
    return processed_data


def get_event_count(preprocessed_data, repo, event_type):
    """
    Get the count of a specific event type for a given repository from preprocessed data.
    """
    if repo in preprocessed_data and event_type in preprocessed_data[repo]:
        return preprocessed_data[repo][event_type]
    return 0


def get_repo_names(events):
    """Get all repos' name and event type fetched and delete duplications."""

    repos = {repo["repo"]["name"] for repo in events}
    return repos


def main():
    # User Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("user", type=str, help="User to get activity from.")
    parser.add_argument("--debug", action="store_true", help="Print all events")

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

        # Preprocess the activity data
        preprocessed_data = preprocess_events(activity)
        for repo, events in preprocessed_data.copy().items():
            print(repo, events)


if __name__ == "__main__":
    main()
