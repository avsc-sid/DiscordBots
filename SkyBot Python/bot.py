from asyncio.windows_events import NULL
import discord
from discord.errors import HTTPException
from discord.ext import commands
import asqlite
from sys import stderr
from traceback import print_exception
from asyncio import run
import discord_slash
import asyncio
import random
import json
import random

bot = commands.Bot(command_prefix="?", help_command=None, description=None, case_insensitive=True, intents=discord.Intents.all(), activity=discord.Activity(type=discord.ActivityType.watching, name='LeaF take the L'))


async def db():
    bot.db = await asqlite.connect("bot.db")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS members (memberID INT PRIMARY KEY, scb INT DEFAULT 0, level INT DEFAULT 0, xp INT DEFAULT 0);")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS shop (itemName TEXT, itemDesc TEXT DEFAULT 0, sellerID INT, price INT DEFAULT 10, itemID INTEGER PRIMARY KEY, inStock INT DEFAULT 0);")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS muted (id INT, guild INT, roles INT, reason TEXT);")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS jokes (id INT, joke TEXT PRIMARY KEY);")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS guild (guild INT PRIMARY KEY, lsRole INT, mutedRole INT, counterChnl INT, unverified INT, prefix TEXT DEFAULT \"!\", scGuild INT DEFAULT 0, countedNum INT DEFAULT 0, xpMulti DEFAULT 1);")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS reaction (msg INT, emoji INT, role INT);")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS bannedWords (word TEXT, guild INT);")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS tags (name TEXT PRIMARY KEY, desc TEXT, user INT);")
    await bot.db.commit()

bot.loop.run_until_complete(db())

bot.colorList = [0x5d8aa8, 0xf0f8ff, 0xe32636, 0xefdecd, 0xe52b50, 0xffbf00, 0xff033e, 0x9966cc, 0xa4c639, 0xf2f3f4, 0xcd9575, 0x915c83]

class HelpCMD(commands.HelpCommand):
    def __init__(self):
        self.verify_checks = False
        self.show_hidden = False
        super().__init__()

    def get_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        r = []
        embed = discord.Embed(title = "Bot commands", colour = random.choice(bot.colorList))
        description = self.context.bot.description + "\n\nTo view help for a specific command, please type `!help [command]`\nTo view help for all categories and commands, please type `!help`"
        if description:
            embed.description = description

        for cog, commands in mapping.items():
            if not cog:
                continue
            filtered = await self.filter_commands(commands, sort = True)
            if filtered:
                for d in filtered:
                    if d.name == "help" or d.name == "ping":
                        print(d.cog)
                        r.append(d)
                value = ",\t".join(f"`{i.name}`" for i in commands)
                embed.add_field(name = cog.qualified_name, value = value)
        embed.add_field(name = "No Category", value = "`help`, `ping`")

        embed.set_footer(text = f"Requested by {self.context.author}", icon_url = self.context.author.avatar.url)
        channel = self.get_destination()
        mesg = await channel.send(embed=embed)
        await mesg.add_reaction("❌")

        def check(reaction, user):
            return user == self.context.message.author and str(reaction.emoji) == "❌"

        try: reaction, user = await self.context.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError: await mesg.clear_reactions()
        else: await mesg.delete()



    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command), color = random.choice(bot.colorList))
        desc = str(command.description)
        if len(desc) == 0:
            desc = 'No description added'
        embed.add_field(name="Description", value=desc)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        a = "No Category"
        if command.cog:
            a = command.cog.qualified_name
        embed.add_field(name="Category", value=a, inline=False)
        embed.description = "To view help for all categories and commands, please type `!help`\nTo view help for a category, please type `!help [category]`"
        embed.set_footer(text = f"Requested by {self.context.author}", icon_url = self.context.author.avatar.url)
        channel = self.get_destination()
        mesg = await channel.send(embed=embed)
        await mesg.add_reaction("❌")

        def check(reaction, user):
            return user == self.context.message.author and str(reaction.emoji) == "❌"

        try: reaction, user = await self.context.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError: await mesg.clear_reactions()
        else: await mesg.delete()


    async def send_error_message(self, error):
        e = self.context.message.content.split(' ')
        a = e[1]
        channel = self.get_destination()
        mesg = await channel.send(f"There was no command or category named `'{a}'`. View `!help` in order to look at all commands and categories.")
        await mesg.add_reaction("❌")

        def check(reaction, user):
            return user == self.context.message.author and str(reaction.emoji) == "❌"

        try: reaction, user = await self.context.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError: await mesg.clear_reactions()
        else: await mesg.delete()


    async def send_cog_help(self, cog):
        a = []
        for c in cog.get_commands():
            a.append(str(c))
        embed = discord.Embed(title=cog.qualified_name, color = random.choice(bot.colorList))
        embed.add_field(name="Commands", value='`' + '`, `'.join(a) + '`')
        embed.description = "To view help for a specific command, please type `!help [command]`\nTo view help for all categories and commands, please type `!help`"
        embed.set_footer(text = f"Requested by {self.context.author}", icon_url = self.context.author.avatar.url)
        channel = self.get_destination()
        mesg = await channel.send(embed=embed)
        await mesg.add_reaction("❌")

        def check(reaction, user):
            return user == self.context.message.author and str(reaction.emoji) == "❌"
        lambda reaction, user: user == self.context.message.author and str(reaction.emoji) == "❌"

        try: reaction, user = await self.context.bot.wait_for('reaction_add', timeout=60.0, check= lambda reaction, user: user == self.context.message.author and str(reaction.emoji) == "❌")
        except asyncio.TimeoutError: await mesg.clear_reactions()
        else: await mesg.delete()

bot.help_command = HelpCMD()


async def role(role, guild):
    async with bot.db.execute(f"SELECT {role} FROM guild WHERE guild = ?;",(guild,)) as cur: roleid = await cur.fetchone()
    role = bot.get_role(roleid[0])
    return role

@bot.event
async def on_ready():
    print('Bot is Ready')


@bot.event
async def on_member_join(user : discord.Member):
    if user.id in [897208996824485949]: return await user.ban(delete_message_days=7, reason="ur a trator")
    print(f'{user} has joined the server')
    unvertified = discord.utils.get(user.guild.roles, name="Unverified") or await role("unverified",user.guild)
    await user.add_roles(unvertified)

@bot.event
async def on_member_remove(user : discord.Member): print(f'{user} has left the server')

@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'): return
    if ctx.cog:
        if ctx.cog._get_overridden_method(ctx.cog.cog_command_error): return

    error = getattr(error, 'original', error)

    if isinstance(error, (commands.CommandNotFound,)): return
    elif isinstance(error, commands.MissingPermissions): return await ctx.send("You are missing permissions.")
    elif isinstance(error, commands.MissingRole): return await ctx.send("You are missing a role.")
    elif isinstance(error, commands.DisabledCommand): return await ctx.send(f'{ctx.command} has been disabled.')
    elif isinstance(error, commands.NoPrivateMessage):
        try: await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
        except Exception: pass
        return
    elif isinstance(error, commands.MessageNotFound): return await ctx.send("That message doesn't exist.")
    elif isinstance(error, commands.GuildNotFound): return await ctx.send("That guild doesn't exist.")
    elif isinstance(error, commands.UserNotFound): return await ctx.send("That user doesn't exist.")
    elif isinstance(error, commands.NoPrivateMessage): return await ctx.send("This command cannot be used in `Private Messages`.")
    elif isinstance(error, commands.CommandOnCooldown): return await ctx.send(f"This command is on cooldown for {int(ctx.command.get_cooldown_retry_after(ctx))} seconds.")

    elif isinstance(error, commands.UserInputError): return await ctx.send_help(ctx.command.qualified_name)
    elif isinstance(error, discord.errors.HTTPException):
        if error.code == 50035: await ctx.reply("I can't send a message that long!")
    msg = await ctx.send("An internal error occurred.")
    await msg.add_reaction("❔")
    try: m, u = await bot.wait_for("reaction_add", check = lambda m, u: u == ctx.author and str(m.emoji) == "❔", timeout=60.0)
    except asyncio.TimeoutError: await msg.clear_reactions()
    else: await ctx.send(error)
    print(f'Ignoring exception in command {ctx.command}:', file=stderr)
    print_exception(type(error), error, error.__traceback__, file=stderr)



@bot.command()
async def ping(ctx): await ctx.send(f':ping_pong: Pong! `{bot.latency*1000} ms`')

# Other files
bot.load_extension("fun")
bot.load_extension("skybucks")
bot.load_extension("utility")
bot.load_extension("music")
bot.load_extension("test")
bot.load_extension("level")
bot.load_extension("guild")
bot.load_extension("dev")

bot.run('token') # SkyBot
#bot.run('token') # SkyBot Test
run(bot.db.commit())
run(bot.db.close())
