# Discord Attendance Bot

## Overview

A discord bot written in python using the discord.py library that handles user attendance.

## Prerequisites

- Python (v3.8+)
- Discord.py (v2.3.2)

## Getting Started

1. Clone this repository:

   ```shell
   git clone https://github.com/MaksimSavich/discord-attendance-bot.git

2. Create a .env file in the base directory:
    ```env
    TOKEN=BOT_TOKEN
3. Ensure that the config file that is generated at the first start looks similar to the content below:
    ```json
    {
        "prefix": "!",
        "autoDeleteDelay": "30",
        "modRoleID": "1234567",
        "guildID": "1234567"
    }

## TODO
- [x] Switch all commands to slash commands
- [ ] Ensure everything works smoothly with slash commands
- [ ] Slash command error handling
- [ ] Finish multi-event setup