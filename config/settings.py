from dotenv import find_dotenv, dotenv_values
from typing import List
from datetime import timedelta

env_path = find_dotenv()

config = dotenv_values(env_path)


class Config:
    DB_URL: str = config['DB_URL']
    DB_MODELS: List[str] = ['models.user']
    SECRET: str = config['JWT_SECRET_KEY']  # ''
    ALGORITHM: str = config['JWT_ALGORITHM']
    JWT_ACCESS_EXP: timedelta = timedelta(days=float(config['JWT_ACCESS_TOKEN_EXP_DAYS']))
    JWT_REFRESH_EXP: timedelta = timedelta(days=float(config['JWT_REFRESH_TOKEN_EXP_DAYS']))
