import discord
from discord.ext.commands import HelpCommand
import random
import asyncio

colorList = [0x5d8aa8, 0xf0f8ff, 0xe32636, 0xefdecd, 0xe52b50, 0xffbf00, 0xff033e, 0x9966cc, 0xa4c639, 0xf2f3f4, 0xcd9575, 0x915c83]

class HelpCMD(HelpCommand):
    def __init__(self):
        self.verify_checks = False
        self.show_hidden = False
        super().__init__()
    
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        r = []
        embed = discord.Embed(title = "Bot commands", colour = random.choice(colorList))
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
         
        embed.set_footer(text = f"Requested by {self.context.author}", icon_url = self.context.author.avatar_url)
        channel = self.get_destination()
        mesg = await channel.send(embed=embed)
        await mesg.add_reaction("❌")

        def check(reaction, user):
            return user == self.context.message.author and str(reaction.emoji) == "❌"

        try: reaction, user = await self.context.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError: await mesg.clear_reactions()
        else: await mesg.delete()



    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command), color = random.choice(colorList))
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
        embed.set_footer(text = f"Requested by {self.context.author}", icon_url = self.context.author.avatar_url)
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
        embed = discord.Embed(title=cog.qualified_name, color = random.choice(colorList))
        embed.add_field(name="Commands", value='`' + '`, `'.join(a) + '`')
        embed.description = "To view help for a specific command, please type `!help [command]`\nTo view help for all categories and commands, please type `!help`"
        embed.set_footer(text = f"Requested by {self.context.author}", icon_url = self.context.author.avatar_url)
        channel = self.get_destination()
        mesg = await channel.send(embed=embed)
        await mesg.add_reaction("❌")

        def check(reaction, user):
            return user == self.context.message.author and str(reaction.emoji) == "❌"
        lambda reaction, user: user == self.context.message.author and str(reaction.emoji) == "❌"

        try: reaction, user = await self.context.bot.wait_for('reaction_add', timeout=60.0, check= lambda reaction, user: user == self.context.message.author and str(reaction.emoji) == "❌")
        except asyncio.TimeoutError: await mesg.clear_reactions()
        else: await mesg.delete()