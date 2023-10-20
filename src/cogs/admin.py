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

    @commands.command(description='test')
    async def fadd(self, ctx, member, name: str):
        df = pd.read_csv('./dataframes/users.csv')
        if (member in df['uuid'].unique()):
            print('Already in db')
            return
        df.loc[len(df.index)] = [name, member]
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