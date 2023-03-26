# GitHub Repository Tag Summarizer

This Python script retrieves the latest 5 tags from a specified GitHub repository, creates summaries for them, saves the
summaries in a `data` directory, and sends notifications to a Slack channel (if enabled).

## Setup

1. If you don't have Poetry installed, install it with:

```
curl -sSL https://install.python-poetry.org | python3 -
```

or follow the installation guide: https://python-poetry.org/docs/#installation

2．Install the required dependencies using Poetry:

```
poetry install
```

3. If you want to use Slack notifications, create a `.env` file in the project root directory and set
   the `SLACK_WEBHOOK_URL` key.

## Usage

1. Make the `run.sh` script executable:

```
chmod +x run.sh
```

2. Run the script with the GitHub username and repository name:

```
./run.sh <username> <repository>
```

If you don't want to use Slack notifications, add the `--no-slack` option:

```
./run.sh <username> <repository> --no-slack
```

3. The script will save the summaries for the latest 5 tags in the `data` directory under the specified username and
   repository.

4. You can set this script as a cron job to run every other day for more convenient use. For example, you can use the
   following cron entry:

```
0 0 */2 * * /path/to/run.sh <username> <repository>
```

