# Github User Activity

The aim of this application is to fetch public events from a Github's user.

## Requirements

- Requests module needs to be installed
```bash
pip3 install requests
```

## Usage

```bash
python3 github_activity.py <username> <options>
```

### Options

| Parameter                    | Description                                                                                         | Default                            
|------------------------------|-----------------------------------------------------------------------------------------------------|---------
| `--debug`                    | Prints all response events                                                                          | false 

### Caveats

For now it only looks up for 

https://roadmap.sh/projects/github-user-activity