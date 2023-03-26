import json
import os

import requests


class SlackMessage:
    def __init__(self):
        self.webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

    def send(self, owner, repo, tag, summary):
        text = f"""
*{owner}/{repo}*: *{tag}*
{summary}
        """
        data = json.dumps({
            "text": text,
            "username": "GithubTagSummarizer"
        })
        response = requests.post(self.webhook_url, data=data)
        if response.status_code != 200:
            raise ValueError(
                f"Request to slack returned an error {response.status_code}, the response is:\n{response.text}"
            )
