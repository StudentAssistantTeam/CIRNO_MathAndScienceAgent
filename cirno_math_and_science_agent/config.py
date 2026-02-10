from pydantic_settings import BaseSettings, SettingsConfigDict

# Settings
class Settings(BaseSettings):
    # a2a config
    a2a_port:str = ""
    a2a_host:str = ""
    # LLM setting
    llm_model_name:str = ""
    llm_base_url:str = ""
    llm_api_key:str = ""
    # Wolfram Setting
    wolfram_app_id:str = ""

    model_config = SettingsConfigDict(
        env_file="../cirno_math_and_science_agent.env",
        env_file_encoding="utf-8",
        extra="allow",
    )

settings = Settings()