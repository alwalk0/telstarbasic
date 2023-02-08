import yaml
import os


main_file = {'host': '0.0.0.0', 'port': 8000, 'app_name': 'my_app', 'models': 'models.py', 'database': 'database', 'templates': 'templates', 'views': 'views2.py'}

with open('main2.yml', 'w') as file:
    document = yaml.dump(main_file, file, sort_keys=False)

views_file = {'home': {'url': '/home', 'endpoint': 'view', 'template': 'index.html'}}

with open('views2.yml', 'w') as file:
    document = yaml.dump(views_file, file, sort_keys=False)    


with open('run1.py', 'w') as f:
    f.write('''\
import uvicorn
import yaml
from framework.parse_yaml import create_app_from_config


MAIN_CONFIG_PATH = 'main.yml'

with open(MAIN_CONFIG_PATH, 'r') as file:
    main_config = yaml.safe_load(file)

app = create_app_from_config(main_config)
host = main_config['host']
port = main_config['port']


if __name__ == "__main__":
    uvicorn.run(app, host=str(host), port=port)
           
''')