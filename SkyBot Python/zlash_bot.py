from discord_slash import SlashCommand, SlashContext
import asyncio
import random
import json
import discord
from discord.ext import menus, commands
from itertools import chain, starmap
from discord.ext.commands.help import Paginator
import random

bot = commands.Bot(command_prefix="!", self_bot=True, help_command=None, intents=discord.Intents.default())
slash = SlashCommand(bot)


bot.load_extension('zlash_cog')
bot.run('token') # SkyBot Test
