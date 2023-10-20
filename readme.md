# Discord Attendance Bot

## Overview

A discord bot written in python using the discord.py library that handles user attendance.

## Prerequisites

- Python (v3.8+)
- Discord.py (v2.3.2)

## Getting Started

1. Clone this repository:

   ```shell
   git clone https://github.com/yourusername/your-project.git

2. Create a .env file in the base directory:
    ```env
    TOKEN=BOT_TOKEN
3. Create a config.json in the ./src directory called config.json (Will be auto-generated in the future):
    ```json
    {
        "prefix": "!",
        "autoDeleteDelay": "30",
        "modRoleID": 1234567
    }