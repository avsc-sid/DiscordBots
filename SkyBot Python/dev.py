from discord.ext import commands
import discord
import random
from requests import get
from bot import HelpCMD


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="request",description="request bug fixes/features",aliases=["bug","feature"])
    async def report(self,ctx,*,bug):
        with open("requests.txt","w") as f: f.write(f"{bug} -{ctx.author}")
        await ctx.send("Thank you for requesting the feature/bug fix!")

    @commands.command(name="about",description="About the bot and the people who helped make it happen") #DO NOT EDIT THIS
    async def about(self, ctx):
        embed = discord.Embed(title="About Me",color=0x154f94)
        embed.set_thumbnail(url=ctx.me.avatar.url)
        embed.add_field(name="Developers",value="Spikestar\nLeafshade\nDarkfang\nDarklord\ndvogit\nAM",inline=False)
        embed.add_field(name="About",value="This bot was created for SkyClan, a group which hangouts out and talks to each other.")
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Dev(bot))