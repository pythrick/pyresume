import json
from functools import lru_cache
from pathlib import Path

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
        credentials_file_path = Path(self.raw_credentials)
        if credentials_file_path.exists():
            return json.load(open(credentials_file_path))
        return json.loads(self.raw_credentials)

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
