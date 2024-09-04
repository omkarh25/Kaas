from github import Github
from github import Auth

class GitHubManager:
    def __init__(self, access_token, repo_name):
        self.auth = Auth.Token(access_token)
        self.g = Github(auth=self.auth)
        self.repo = self.g.get_repo(repo_name)

    def get_issues(self, state="all"):
        return self.repo.get_issues(state=state)

    def create_issue(self, title, body):
        return self.repo.create_issue(title=title, body=body)

    def close_issue(self, issue_number):
        issue = self.repo.get_issue(number=issue_number)
        issue.edit(state="closed")

    def add_comment(self, issue_number, comment):
        issue = self.repo.get_issue(number=issue_number)
        issue.create_comment(comment)