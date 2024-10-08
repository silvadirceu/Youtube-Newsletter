from pydantic_settings import BaseSettings


class GeneralSettings(BaseSettings):
    PROJECT_NAME: str = "Youtube Newsletter API"
    PROJECT_DESCRIPTION: str = "Youtube Newsletter API for automate the generation of newssleters from Youtube"
    TAG: str = "2.0"
    VERSION: str = TAG

    class Config:
        case_sensitive = True
        extra = "allow"
