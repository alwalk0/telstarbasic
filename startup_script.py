import yaml
import os


main_file = {'host': '0.0.0.0', 'port': 8000, 'models': 'models.py', 'database': 'database', 'endpoints': {'hello_world':{'url': '/', 'method':'GET'} }}

with open('main.yml', 'w') as file:
    document = yaml.dump(main_file, file, sort_keys=False)


