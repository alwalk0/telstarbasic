import uvicorn
from framework.parse_yaml import create_app_from_config, read_key_from_config


MAIN_CONFIG_PATH = 'main.yml'

views_config_name = read_key_from_config(MAIN_CONFIG_PATH, 'views')

app = create_app_from_config(views_config_name)
host = read_key_from_config(MAIN_CONFIG_PATH, 'host')
port = read_key_from_config(MAIN_CONFIG_PATH, 'port')


if __name__ == "__main__":
    uvicorn.run(app, host=str(host), port=port)
    