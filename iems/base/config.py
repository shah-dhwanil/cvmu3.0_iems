from pydantic import BaseModel
from tomllib import load
from dotenv import load_dotenv
from os import environ

config = None


class Config(BaseModel):
    SERVER_ENVIRONMENT: str
    SERVER_HOST: str
    SERVER_PORT: int
    POSTGRES_DSN: str
    POSTGRES_MIN_CONN: int
    POSTGRES_MAX_CONN: int
    PASETO_SECRET_KEY: str
    PUBLIC_ROUTES: list[str]
    BRANCH_LIST: list[str]

    @staticmethod
    def __get_toml_config(environment: str):
        config = {}
        with open("config.toml", "rb") as fp:
            toml_config = load(fp)
            config.update(toml_config["DEFAULT"])
            config.update(toml_config[environment])
        return config

    @staticmethod
    def __get_env_config(environment: str):
        config = {}
        load_dotenv(f"{environment.lower()}.env")
        config.update()
        for key in environ:
            if key.startswith("IEMS"):
                config[key.removeprefix("IEMS_")] = environ[key]
        return config

    @classmethod
    def get_config(cls):
        global config
        if not config:
            load_dotenv(".env")
            environment = environ["IEMS_SERVER_ENVIRONMENT"]
            config = cls.__get_toml_config(environment)
            config.update(cls.__get_env_config(environment))
            config["SERVER_ENVIRONMENT"] = environment
            config = cls(**config)
        return config
