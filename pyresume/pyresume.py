import json

from config import get_settings

from pyresume.db import get_resume
from pyresume.github import push_file

settings = get_settings()


def get_resume_from_database(db):
    return get_resume(db)


def push_resume(git, resume: dict):
    content = json.dumps(resume)
    push_file(git, content, "resume.json", "Update resume content")


def update_resume(db, git):
    resume = get_resume_from_database(db)
    push_resume(git, resume)
