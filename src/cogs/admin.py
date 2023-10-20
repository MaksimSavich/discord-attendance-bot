import discord
import pandas as pd
import settings, syscommands
import asyncio
import random
from discord.ext import commands

class admin(commands.Cog, description='Administration commands'):

    def __init__(self, bot):
        self.bot = bot

    # Variable that is set equal to the output from the bot so that it can be deleted after the cog is invoked
    msg = None

    # Purge command
    @commands.command(description='Purges chat')
    async def purge(self, ctx, amount: int):
        async for message in ctx.channel.history(limit=amount):
            delay = random.random()
            await asyncio.sleep(delay)
            await message.delete()

    # Reboot command
    @commands.command(description='Reboots bot')
    async def reboot(self, ctx):
        await ctx.send('```ini\nRebooting...\n```')
        syscommands.reboot()

    @commands.command(description='Force adds a new user to the users database')
    async def fadd(self, ctx, member, *name: str):
        df = pd.read_csv('./dataframes/users.csv')
        if (member in df['uuid'].unique()):
            await ctx.send('```ini\nThis user has already signed up.\n```')
            return
        df.loc[len(df.index)] = [name, member]
        df.to_csv('./dataframes/users.csv', index=False)
        await ctx.send('```ini\nThe user has been added.\n```')

    @commands.command(description='Changes name of the user in the users database')
    async def changename(self, ctx, member: int, *name:str):
        df = pd.read_csv('./dataframes/users.csv')
        df.loc[df[df['uuid'] == member].index[0], 'name'] = f'{name}'
        df.to_csv('./dataframes/users.csv', index=False)

    # Deletes the command sent by the bot
    async def cog_before_invoke(self, ctx):
        await ctx.message.delete()

    # Deletes the output from the bot after a certain amount of time
    async def cog_after_invoke(self, ctx):
        if self.msg != None:
            await asyncio.sleep(settings.autoDeleteDelay)
            try:
                await self.msg.delete()
            except:
                pass
            self.msg = None

# Registers the cog
async def setup(bot):
    await bot.add_cog(admin(bot))