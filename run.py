import uvicorn
from framework.parse_yaml import create_app_from_config, parse_main_config, read_key_from_config



app = create_app_from_config('views.yml')


host = read_key_from_config('main.yml', 'host')
port = read_key_from_config('main.yml', 'port')


if __name__ == "__main__":
    uvicorn.run(app, host=str(host), port=port)
    