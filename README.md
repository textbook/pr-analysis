# Pull Request Analysis

How long does it take to merge PRs?

## Installation

Clone the repository to your local machine.

Dependencies are listed in `requirements.txt`. We recommend installing them in a virtualenv:

```shell
$ python3 -m venv ~/.virtualenvs/pr-analysis
$ source ~/.virtualenvs/pr-analysis/bin/activate
$ pip install -r requirements.txt
```

## Usage

Run `cli.py` and pass the appropriate arguments:

```shell
$ ./cli.py --help
usage: cli.py [-h] [--created-after CREATED_AFTER] [--csv CSV] [--json JSON]
              [--limit LIMIT] [--merged-before MERGED_BEFORE] [--pretty]
              [--quiet]
              owner repo

Perform statistical analysis on merged pull requests

positional arguments:
  owner                 Org or user
  repo                  Repository

options:
  -h, --help            show this help message and exit
  --created-after CREATED_AFTER
                        Filter by creation date
  --csv CSV             Save PR data to CSV file
  --json JSON           Save PR data to JSON file
  --limit LIMIT         Number of PRs to analyse
  --merged-before MERGED_BEFORE
                        Filter by merge date
  --pretty              Human-readable JSON
  --quiet               Suppress printed outputs
```

**Note** the CLI expects a valid [personal access token] (with the `repo` scope) as the `GITHUB_PAT` environment variable.

For example, to analyse the last 500 merged PRs and save in a human-readable JSON file:

```shell
GITHUB_PAT=<token> ./cli.py <org/user> <repo> --json path/to/output.json --limit=500 --pretty
```

[personal access token]: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
