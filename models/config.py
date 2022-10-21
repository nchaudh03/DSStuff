
from dynaconf import Dynaconf
from models.src.helpers.utility import make_logger
logger = make_logger()


settings = Dynaconf(
    envvar_prefix="CRR",
    settings_files=['settings.toml', '.secrets.toml'],
    environments=['dev', 'prod'],
    env_switcher="ENV",
)
