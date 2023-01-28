import uvicorn
from framework.parse_yaml import create_app_from_config


app = create_app_from_config('config.yml')


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
    