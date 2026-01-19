import discord
from discord.ext import commands
from bot import HelpCMD

class Guild(commands.Cog):
    def __init__(self,bot): #guild INT PRIMARY KEY, lsRole INT, mutedRole INT, counterChnl INT, unverified INT, prefix TEXT DEFAULT \"!\", scGuild INT, countedNum INT DEFAULT 0, xpMulti DEFAULT 1
        self.bot = bot
        
    async def power(self,user):
        await self.bot.wait_until_ready()
        async with self.bot.db.execute(f"SELECT guild FROM guild WhERE scGuild = 1;") as cur: guilds = await cur.fetchall()
        for r in guilds:
            guild = self.bot.get_guild(r[0])
            leadership = discord.utils.get(guild.roles, name="Leadership_Roles") or await self.role("lsRole",guild)
            if leadership in user.roles: return True
        return False

    @commands.command(name="set",description="Set a specific item to your choice. The current items are leadership roles, muted roles, counting channel, unverified role, prefix, and whether it is an official skyclan guild or not.")
    async def set(self, ctx, *, item):
        await ctx.send("Type what to set it to. (if it is True/False True is 1 and False is 0)")
        to = await self.bot.wait_for("message",check = lambda msg: msg.channel == ctx.channel and msg.author == ctx.author)
        if item.lower() in ["leadership role","lsrole","leadership","leadershiprole","leadership roles"]: column = "lsRole"
        elif item.lower() in ["muted","mutedrole","muted role"]: column = "mutedRole"
        elif item.lower() in ["counterchnl","counting channel","countingchannel","countrchannel"]: column = "counterChnl"
        elif item.lower() in ["unverified","unverified role","unverifiedrole"]: column = "unverified"
        elif item.lower() in ["prefix","official prefix"]: column = "prefix"
        elif item.lower() in ["skyclan guild","skyclanguild","sky clan guild","scguild","sc guild","osd"]: 
            if await self.power(ctx.author): 
                await self.bot.db.execute("UPDATE guild SET scGuild = ? WHERE guild = ?;",(int(to),ctx.guild.id))
                return await ctx.send("Set `scGuild` to True :thumbsup:")
            else: return await ctx.send(f"{ctx.author.mention}, you don't have the permissions for that.")
        else: return await ctx.send("The options are `lsRole` `mutedRole` `counterChnl` `unverified` `prefix` or `scGuild`")

        if ctx.author.guild_permissions.administrator: 
            await self.bot.db.execute(f"UPDATE guild SET {column} = ? WHERE guild = ?;",(int(to),ctx.guild.id))
            return await ctx.send(f":thumbsup: Successfully set **{column}** to `{to}`")
        else: return await ctx.send(f"{ctx.author.mention}, you need administrator to perform this action.")



    @commands.command(name="serversetup",description="Sets up the server! This command should be run first",aliases=["ssetup","setup"])
    async def ssetup(self, ctx):
        await ctx.send("This will reset all your current data. However, you can type `None` if you would not like to change the defaults. Mention the correct role/channel after each message!")
        try: await self.bot.db.execute("INSERT INTO guild (guild) VALUES (?);",(ctx.guild.id,))
        except Exception: pass

        await ctx.send("Leadership Role")
        msg = await self.bot.wait_for("message",check = lambda msg: msg.channel == ctx.channel and msg.author == ctx.author)
        item = await commands.RoleConverter().convert(ctx, msg.content)
        if not "none" in msg.content.lower(): await self.bot.db.execute("UPDATE guild SET lsRole = ? WHERE guild = ?;",(item.id,ctx.guild.id))

        await ctx.send("Muted Role")
        msg = await self.bot.wait_for("message",check = lambda msg: msg.channel == ctx.channel and msg.author == ctx.author)
        item = await commands.RoleConverter().convert(ctx, msg.content)
        if not "none" in msg.content.lower(): await self.bot.db.execute("UPDATE guild SET mutedRole = ? WHERE guild = ?;",(item.id,ctx.guild.id))

        await ctx.send("Counting Channel")
        msg = await self.bot.wait_for("message",check = lambda msg: msg.channel == ctx.channel and msg.author == ctx.author)
        item = await commands.TextChannelConverter().convert(ctx, msg.content)
        if not "none" in msg.content.lower(): await self.bot.db.execute("UPDATE guild SET counterChnl = ? WHERE guild = ?;",(item.id,ctx.guild.id))

        await ctx.send("Unverified Role")
        msg = await self.bot.wait_for("message",check = lambda msg: msg.channel == ctx.channel and msg.author == ctx.author)
        item = await commands.RoleConverter().convert(ctx, msg.content)
        if not "none" in msg.content.lower(): await self.bot.db.execute("UPDATE guild SET unverified = ? WHERE guild = ?;",(item.id,ctx.guild.id))

        await ctx.send("Prefix")
        msg = await self.bot.wait_for("message",check = lambda msg: msg.channel == ctx.channel and msg.author == ctx.author)
        if not "none" in msg.content.lower(): await self.bot.db.execute("UPDATE guild SET prefix = ? WHERE guild = ?;",(msg.content,ctx.guild.id))

        async with self.bot.db.execute("SELECT lsRole, mutedRole, counterChnl, unverified, prefix FROM guild WHERE guild = ?;",(ctx.guild.id,)) as cur: stuff = await cur.fetchone()
        embed = discord.Embed(title="Server Successfully Set up!",color=0x134E41)
        embed.add_field(name="Leadership Role",value=ctx.guild.get_role(stuff[0]))
        embed.add_field(name="Muted Role",value=ctx.guild.get_role(stuff[1]))
        embed.add_field(name="Counting channel",value=ctx.guild.get_channel(stuff[2]))
        embed.add_field(name="Unverified Role",value=ctx.guild.get_role(stuff[3]),inline=False)
        embed.add_field(name="Prefix",value=stuff[4])
        a = "https://cdn.discordapp.com/icons/921230858311057418/4906a069ad5db4026d9bc068c316c291.webp?size=1024"
        if ctx.guild.icon != None: a = ctx.guild.icon.url
        embed.set_thumbnail(url=a)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction, user):
        async with self.bot.db.execute("SELECT * FROM reaction;") as cur: list = await cur.fetchall()
        for item in list:
            emoji = reaction.emoji
            if reaction.message.id == item[0] and emoji.id == item[1]: #do i use reaction.emoji.id? 
                role = user.guild.get_role(item[2])
                return await user.add_roles(role)


    @commands.command(name="reaction",description="add a new reaction role")
    async def reaction(self,ctx):
        await ctx.send("What is the message ID of the reaction role?")
        message = await self.bot.wait_for("message",check = lambda msg: msg.channel == ctx.channel and msg.author == ctx.author and msg.content.isnumeric())

        await ctx.send("The reaction:")
        emoji = await self.bot.wait_for("message",check = lambda msg: msg.channel == ctx.channel and msg.author == ctx.author)
        em = await commands.EmojiConverter().convert(ctx, emoji)

        await ctx.send("The role the user would get:")
        role = await self.bot.wait_for("message",check = lambda msg: msg.channel == ctx.channel and msg.author == ctx.author)
        item = await commands.RoleConverter().convert(ctx, role.content)
        #how do you parse this for multiple roles

        await self.bot.db.execute("INSERT INTO reaction VALUES (?,?,?);",(message,em.id,item.id)) #idk emoji


def setup(bot):
    bot.add_cog(Guild(bot))