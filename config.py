import json
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    spreadsheet: str
    raw_credentials: str
    github_token: str
    repository_name: str
    git_author_name: str
    git_author_email: str

    @property
    def credentials(self) -> str:
        return json.loads(self.raw_credentials)

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
