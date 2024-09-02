from typing import Any, Dict, List, Optional

from pydantic import EmailStr, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        env_file=('.env', '.env.prod'),
        extra='ignore'
    )

    # Project and API version
    PROJECT_NAME: str = "InnoCore"
    PROJECT_DESCRIPTION: str = "InnoVox ChatBot Builder Core'"
    API_PROXY_STR: str = ""
    ROOT_PATH: str = ""
    
    # CHATGPT API
    CHATGPT_API_KEY: str = ""
    CHATGPT_MODEL: str = "gpt-3.5-turbo-1106"
    CHATGPT_TEMPERATURE: float = .2

    # Email server settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 465
    SMTP_HOST: Optional[str] = 'mail.innovox.ai'
    SMTP_USER: Optional[str] = 'no-reply-test@innovox.ai'
    SMTP_PASSWORD: Optional[str] = 'kasdkj29jlasd9'
    EMAILS_FROM_EMAIL: Optional[EmailStr] = 'no-reply-test@innovox.ai'
    EMAILS_FROM_NAME: Optional[str] = 'No-Reply-Email-Test'

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    # Recovering password
    FRONT_END_HOST: str = 'localhost:4200'

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "./innocore/email-templates/build"  # "/code/./innocore/email-templates/build"
    EMAILS_ENABLED: bool = True

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    # Original data in database
    FIRST_SUPERUSER: EmailStr = "cesar.medina@innovox.com.br"
    FIRST_SUPERUSER_NAME: str = "César Medina"
    FIRST_SUPERUSER_PASSWORD: str = "cesarmedina"

    ROLES: List[str] = ["SysAdmin", "SysUser", "Admin", "User", "ApiUser"]


settings = Settings()
