from functools import lru_cache

import github as gh
from github import InputGitAuthor

from config import get_settings


settings = get_settings()


def get_author() -> InputGitAuthor:
    return InputGitAuthor(settings.git_author_name, settings.git_author_email)


def push_file(git, content: str, file_path: str, commit_message: str):
    repo = git.get_repo(settings.repository_name)
    branch = repo.default_branch
    author = get_author()
    try:
        contents = repo.get_contents(file_path)
        repo.update_file(
            contents.path,
            commit_message,
            content,
            contents.sha,
            branch=branch,
            author=author,
        )
    except gh.UnknownObjectException:
        repo.create_file(
            file_path, commit_message, content, branch=branch, author=author
        )


@lru_cache()
def get_github():
    return gh.Github(settings.github_token)
