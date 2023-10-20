import os
import pathlib
import json

if not os.path.isfile('./src/config.json'):
    data = {
        "prefix": "!",
        "autoDeleteDelay": "30",
        "modRoleID": "1234567"
    }
    json_object = json.dumps(data, indent=4)
    with open("./src/config.json", "w") as outfile:
        outfile.write(json_object)


# Sets BASE_DIR = to the base directory
BASE_DIR = pathlib.Path(__file__).parent

# Sets COGS_DIR = to the cogs directory
COGS_DIR = BASE_DIR / 'cogs'

# Sets COBNFIG_DIR = to the config.json file
CONFIG_DIR = BASE_DIR / 'config.json'

# Opens config.json
with open(CONFIG_DIR, "r") as file:
    config = json.load(file)

# Variables that are set equal to the value of the key they are named the same ass
prefix = config['prefix']
autoDeleteDelay = int(config['autoDeleteDelay'])
modRoleID = int(config['modRoleID'])

# Function that modifies the value of a key value pair in config.json
async def modifyConfig(key, value):
    config[f'{key}'] = value
    with open(CONFIG_DIR, 'w') as file:
        json.dump(config, file, indent=4)