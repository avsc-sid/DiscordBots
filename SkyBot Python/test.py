import discord
from discord.ext import commands
import sqlite3
from bot import HelpCMD

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(name = "admintest", description="A test to see if it'll return you are admin or not.")
    async def admintest(self, ctx):
        if ctx.author.guild_permissions.administrator: await ctx.send("Ur an admin")
        else: await ctx.send("L")
    
    @commands.command(name = "test", description = "prints to the console.")
    async def test(self, ctx): print(ctx.guild)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id=payload.message_id
        emoji=None
        if int(message_id)==893965308644188301:
            emoji=payload.emoji.name
        if emoji=='\U0001f511':
            user=payload.member
            DJ = discord.utils.get(user.guild.roles, name="DJ")
            await user.add_roles(DJ)

    @commands.command(name = "writeSQL", description = "this is a test to write to an sql file")
    async def writesql(self, ctx, arg):
        try:
            con = sqlite3.connect(":memory:")
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS test (idk TEXT)")
            cur.execute("INSERT INTO test VALUES (?)", (arg,))

            con.commit()
            con.close()
            await ctx.send(f"Thanks for your input {ctx.author.mention}!")
        except Exception: await ctx.send(f"{ctx.author.mention}, see `!help writeSQL`")

    @commands.command(name = "typename", description="A test command that will ask for you to enter your name.")
    async def hello(self, ctx):
        await ctx.send("Type your name...")
        msg = await commands.wait_for("message")
        await ctx.send(f'hello, {msg.content}')
    
    @commands.command(name="highrole")
    async def highrole(self, ctx, user : discord.Member):
        await ctx.send(ctx.author.top_role > user.top_role)

def setup(bot):
    bot.add_cog(Test(bot))