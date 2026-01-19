from discord.ext import commands
from help import HelpCMD

bot = commands.Bot(command_prefix="?", help_command=HelpCMD(), description=None, self_bot=False, case_insensitive=True, owner_id=667760867483582492)

bot.colorList = [0x5d8aa8, 0xf0f8ff, 0xe32636, 0xefdecd, 0xe52b50, 0xffbf00, 0xff033e, 0x9966cc, 0xa4c639, 0xf2f3f4, 0xcd9575, 0x915c83]

@bot.event
async def on_ready():
    print("Ready")

bot.load_extension("cmds")

bot.run("token")
