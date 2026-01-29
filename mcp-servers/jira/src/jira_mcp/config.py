from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    jira_url: str
    jira_email: str
    jira_api_token: str

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
