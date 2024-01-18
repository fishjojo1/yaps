import os
import json
import argparse
from proxy import app
from tinydb import TinyDB

def main():
    # get json config file from cmd arguments
    parser = argparse.ArgumentParser(description='Startup Args')
    parser.add_argument('--config', type=str, default='config.json', help='config file path')
    args = parser.parse_args()
    config_path = args.config

    # loads config file
    if not os.path.isfile(config_path):
        raise Exception('Config file not found')

    else:
        with open(config_path, 'r') as f:
            config = json.load(f)



    # start web proxy
    db = TinyDB(config['db-path'])
    app.config['db'] = db
    app.config['options'] = config['log-info']
    app.run(port=config['proxy-port'])
    



if __name__ == '__main__':
    main()
