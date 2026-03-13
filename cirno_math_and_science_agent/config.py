from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / "cirno_math_and_science_agent.env"


# Settings
class Settings(BaseSettings):
    # a2a config
    a2a_port: int = 4000
    a2a_host: str = ""
    use_db_push_notifications: bool = False
    use_db_task_store: bool = False
    db_url: str = ""
    # LLM setting
    llm_model_name: str = ""
    llm_base_url: str = ""
    llm_api_key: str = ""
    llm_provider: str = ""
    # Wolfram Setting
    wolfram_app_id: str = ""
    # OpenAlex Setting
    openalex_api: str = ""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="allow",
    )


settings = Settings()
