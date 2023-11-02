import os
import pathlib
import json

# Sets BASE_DIR = to the base directory
BASE_DIR = pathlib.Path(__file__).parent

# Sets COGS_DIR = to the cogs directory
COGS_DIR = BASE_DIR / 'cogs'

# Sets COBNFIG_DIR = to the config.json file
CONFIG_DIR = BASE_DIR / 'config.json'

# Generates a config.json file if one doesn't exist
if not os.path.isfile(CONFIG_DIR):
    data = {
        "prefix": "!",
        "modRoleID": "123",
        "guildID": "123",
        "attendanceChannel": "123",
        "attendanceOutputChannel": "123"
    }
    json_object = json.dumps(data, indent=4)
    with open(CONFIG_DIR, "w") as outfile:
        outfile.write(json_object)


# Opens config.json
with open(CONFIG_DIR, "r") as file:
    config = json.load(file)

# Variables that are set equal to the value of the key they are named the same as
prefix = config['prefix']
modRoleID = int(config['modRoleID'])
guildID = int(config['guildID'])
attendanceChannel = int(config['attendanceChannel'])
attendanceOutputChannel = int(config['attendanceOutputChannel'])

# Function that modifies the value of a key value pair in config.json
async def modifyConfig(key, value):
    config[f'{key}'] = value
    with open(CONFIG_DIR, 'w') as file:
        json.dump(config, file, indent=4)