import discord
import os
import settings, permissions
import asyncio
import pandas as pd
from discord.ext import commands
from discord import app_commands

class general(commands.Cog, description='General commands'):

    def __init__(self, bot):
        self.bot = bot

    # Variable that is set equal to the output from the bot so that it can be deleted after the cog is invoked
    msg = None

    @commands.command(description='Signs a user up for the attendance bot')
    async def signup(self, ctx, *name: str):
        df = pd.read_csv('./dataframes/users.csv')
        if (ctx.message.author.id in df['uuid'].unique()):
            await ctx.send('```ini\nYou have already signed up.\n```')
            return
        df.loc[len(df.index)] = [' '.join(name), ctx.message.author.id]
        df.to_csv('./dataframes/users.csv', index=False)
        await ctx.send('```ini\nYou have signed up.\n```')

    @app_commands.command(name="cog-mannu",description="Mannu is in a good cog")
    @app_commands.check(permissions.is_mod)
    async def slash_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("IM IN A COG!")

    # Deletes the command sent by the user
    # async def cog_before_invoke(self, ctx):
    #     await ctx.message.delete()

    # Deletes the output from the bot after a certain amount of time
    # async def cog_after_invoke(self, ctx):
    #     if self.msg != None:
    #         await asyncio.sleep(settings.autoDeleteDelay)
    #         try:
    #             await self.msg.delete()
    #         except:
    #             pass
    #         self.msg = None

# Registers the cog
async def setup(bot):
    await bot.add_cog(
        general(bot),
        guilds = [discord.Object(id=819420666615955457)]  
        )