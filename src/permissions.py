import settings
from discord.ext import commands

def is_admin(ctx):
    # Check if the user invoking the command has admin permissions
    return ctx.author.guild_permissions.manage_guild

def is_mod(ctx):
    # Check if the user invoking the command has a specific role ID
    return settings.modRoleID in [role.id for role in ctx.author.roles]