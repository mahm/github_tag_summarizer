import os
import argparse
from dotenv import load_dotenv

from github import Github
from slack_message import SlackMessage
from tag_summarizer import TagSummarizer


def process_tags(owner, repo, tag_pairs):
    for tag_pair in tag_pairs:
        process_tag(owner, repo, tag_pair)


def process_tag(owner, repo, tag_pair):
    tag_name = tag_pair[0]
    prev_tag_name = tag_pair[1]
    dir_path = f"./data/{owner}/{repo}/{tag_name}"
    summary_path = f"{dir_path}/summary.txt"
    if not is_file_exist(summary_path):
        print(f"Processing tags {tag_name} for {owner}/{repo}")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        tag_summarizer = TagSummarizer(owner, repo, tag_name, prev_tag_name)
        summary = tag_summarizer.summarize()
        print('----------------------------------------')
        print(summary)
        print('----------------------------------------')
        with open(summary_path, "w") as f:
            f.write(summary)
        send_to_slack(owner, repo, tag_name, summary)


def send_to_slack(owner, repo, tag_name, summary):
    slack_message = SlackMessage()
    slack_message.send(owner, repo, tag_name, summary)


def is_file_exist(path):
    return os.path.exists(path) and os.path.isfile(path)


def main(args):
    github = Github(args.owner, args.repo)
    tag_pairs = github.get_latest_and_previous_tags()
    process_tags(args.owner, args.repo, tag_pairs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process GitHub repository tags and create summaries.')
    parser.add_argument('owner', type=str, help='GitHub repository owner')
    parser.add_argument('repo', type=str, help='GitHub repository name')
    args = parser.parse_args()

    load_dotenv()
    main(args)
