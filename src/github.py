import os
from collections import defaultdict

import requests
from bs4 import BeautifulSoup


class Github:
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo

    def get_latest_and_previous_tags(self, num_pairs=5):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/tags"
        response = requests.get(url)
        tags = response.json()
        tag_pairs = [(tags[i]['name'], tags[i + 1]['name']) for i in range(num_pairs)]
        return tag_pairs

    def get_release_description(self, tag):
        url = f"https://github.com/{self.owner}/{self.repo}/releases/tag/{tag}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find('div', class_='markdown-body').get_text(strip=True)

    def extract_tag_differences(self, tag, prev_tag):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/compare/{prev_tag}...{tag}"
        response = requests.get(url)
        compare_data = response.json()

        groups = defaultdict(list)
        for file in compare_data["files"]:
            if "patch" in file:
                ext = os.path.splitext(file["filename"])[-1]
                groups[ext].append({"filename": file["filename"], "patch": file["patch"]})

        return groups
