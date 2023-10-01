from fastapi import FastAPI
from starlette.responses import JSONResponse
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

app = FastAPI(title="Fastapi_Games",
              version="0.1",
              description="проект на fasapi c tortoise ORM")


@app.get("/get")
async def docs():
    return JSONResponse({'message': 'Hello World'})


class SiteSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8', env_prefix='SITE_')
    host: str = Field("0.0.0.0", alias="SITE_HOST")
    port: int = Field(8080, alias="SITE_PORT")


settings_site = SiteSettings()


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8', env_prefix='DATABASE_')
    user: str = Field(alias='DATABASE_USER')
    password: str = Field(alias='DATABASE_PASSWORD')
    host: str = Field('localhost', alias='DATABASE_HOST')
    name: str = Field(alias='DATABASE_NAME')
    port: str = Field(alias='DATABASE_PORT')


class DataBaseConnections(BaseSettings):
    default: str = Field("postgres://{user}:{password}@{host}:{port}/{name}")

    @field_validator("default")
    def generate_db_url(cls, db_url: str):
        print()
        return db_url.format(**PostgresSettings().model_dump())


database_url: str = DataBaseConnections().default
print()


class TortoiseSettings(BaseSettings):
    generate_schemas: bool = Field(True, env="TORTOISE_GENERATE_SCHEMAS")
    add_exception_handlers: bool = Field(True, env="DATABASE_EXCEPTION_HANDLERS")

