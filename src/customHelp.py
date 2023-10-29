import settings, re
import asyncio
from discord.ext import commands

# Custom help command handler
class customHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        await self.context.message.delete()
        cogs = ''
        for cog in mapping:
            if (cog != None):
                cogs += f'[{cog.qualified_name}] {cog.description}\n'
        res = f'```ini\n[ Solar Attendance ]\n\n<> = required, [] = optional\n{settings.prefix}help [command]\n\n{cogs}```'
        msg = await self.get_destination().send(res)
        await asyncio.sleep(settings.autoDeleteDelay)
        try:
            await msg.delete()
        except:
            pass
                
    async def send_cog_help(self, cog):
        await self.context.message.delete()
        cmds = ''
        for command in cog.get_commands():
            cs = re.sub(r'=(.*?)]', r']', command.signature)
            cmds += f'[{settings.prefix}{command.name} {cs}] {command.description}\n'
        res = f'```ini\n{cog.qualified_name.capitalize()}\n\n<> = required, [] = optional\n{settings.prefix}help [command]\n\n{cmds}```'
        msg = await self.get_destination().send(res)
        await asyncio.sleep(settings.autoDeleteDelay)
        try:
            await msg.delete()
        except:
            pass

    # Not sure if we want to do a global group help or customize the help within each cog
    # async def send_group_help(self, group):
    #     gcmds = ''
    #     for command in enumerate(group.commands):
    #         gcmds += '[ ' + f'{settings.prefix}' + command.name + ' ] ' + command.description + '\n'
    #     res = f'```ini\n[ Solar Attendance ]\n\n<> = required, [] optional\n{settings.prefix}help [command]\n\n{gcmds}```'
    #     await self.get_destination().send(res)

    async def send_command_help(self, command):
        await self.context.message.delete()
        msg = await self.get_destination().send(f'```ini\n{command.description}\n```')
        await asyncio.sleep(settings.autoDeleteDelay)
        try:
            await msg.delete()
        except:
            pass