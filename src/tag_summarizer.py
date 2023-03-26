import requests
import tiktoken
from tiktoken.core import Encoding
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)
from langchain.text_splitter import NLTKTextSplitter
import templates as t
from github import Github

MODEL_NAME = "gpt-3.5-turbo"
MAX_TOKENS_LIMIT = 3375


def token_count(text):
    encoding: Encoding = tiktoken.encoding_for_model(MODEL_NAME)
    return len(encoding.encode(text))


class TagSummarizer:
    def __init__(self, owner, repo, tag, prev_tag):
        self.owner = owner
        self.repo = repo
        self.tag = tag
        self.prev_tag = prev_tag
        self.github = Github(owner, repo)

    def summarize(self):
        groups = self.github.extract_tag_differences(self.tag, self.prev_tag)
        group_summaries = self.process_each_ext(groups)
        return self.process_overall("\n".join(group_summaries.values()))

    def summarize_each_file(self, filename, changes_text):
        llm = ChatOpenAI(temperature=0)
        result = llm([HumanMessage(content=t.each_file_prompt().format(filename=filename, text=changes_text))])
        return result.content

    def summarize_each_ext(self, text_array):
        llm = ChatOpenAI(temperature=0.4)
        tag_desc = self.github.get_release_description(self.tag)
        result = llm([HumanMessage(content=t.each_ext_prompt().format(desc=tag_desc, text="\n".join(text_array)))])
        return result.content

    def summarize_overall(self, text):
        llm = ChatOpenAI(temperature=0.4)
        tag_desc = self.github.get_release_description(self.tag)
        result = llm([HumanMessage(content=t.overall_prompt().format(desc=tag_desc, text=text))])
        return result.content

    def process_overall(self, text):
        token = token_count(text)
        if token <= MAX_TOKENS_LIMIT:
            return self.summarize_overall(text)
        text_splitter = NLTKTextSplitter(chunk_size=MAX_TOKENS_LIMIT)
        chunks = text_splitter.split_text(text)
        summarized_chunks = [self.summarize_overall(chunk) for chunk in chunks]
        combined_summary = "\n".join(summarized_chunks)
        self.process_overall(combined_summary)

    def process_each_ext(self, groups):
        group_summaries = {}
        for ext, patches in groups.items():
            summaries = []
            for patch in patches:
                filename = patch['filename']
                diff_lines = patch['patch'].splitlines()
                result = self.process_each_file(filename, diff_lines)
                summaries.append(result)
            group_summaries[ext] = self.summarize_each_ext(summaries)
        return group_summaries

    def process_each_file(self, filename, diff_lines):
        _lines = []

        for line in diff_lines:
            if line.startswith('+') or line.startswith('-'):
                _lines.append(line[1:])
            else:
                _lines.append(line)

        tokens = [
            token_count(line)
            for line in _lines
        ]
        total_token = sum(tokens)
        num_lines = len(_lines)
        while total_token > MAX_TOKENS_LIMIT:
            num_lines -= 1
            total_token -= tokens[num_lines]
        input_text = '\n'.join([f"{line}" for line in _lines[:num_lines]])
        summary = self.summarize_each_file(filename, input_text)
        return summary
