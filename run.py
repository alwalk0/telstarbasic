import uvicorn
import yaml
from framework.parse_yaml import create_app_from_config, read_key_from_config


MAIN_CONFIG_PATH = 'main.yml'

with open(MAIN_CONFIG_PATH, 'r') as file:
    main_config = yaml.safe_load(file)

app = create_app_from_config(main_config)
host = main_config['host']
port = main_config['port']


if __name__ == "__main__":
    uvicorn.run(app, host=str(host), port=port)
    