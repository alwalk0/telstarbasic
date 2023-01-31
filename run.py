import uvicorn
from framework.parse_yaml import create_app_from_config, parse_main_config


port, host, models, templates, views, database = parse_main_config('main.yml')

app = create_app_from_config('views.yml', models, templates, views)


if __name__ == "__main__":
    uvicorn.run(app, host=str(host), port=port)
    