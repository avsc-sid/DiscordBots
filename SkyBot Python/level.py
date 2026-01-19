import discord
from discord.ext import commands
from random import randint
from bot import HelpCMD
from math import floor

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_cooldown = commands.CooldownMapping.from_cooldown(1.0, 60.0, commands.BucketType.user)

    async def role(self, role : str, guild):
        async with self.bot.db.execute(f"SELECT {role} FROM guild WHERE guild = ?",(guild,)) as cur: roleid = await cur.fetchone()
        role = self.bot.get_role(roleid[0])
        return role
    
    async def power(self,user):
        await self.bot.wait_until_ready()
        async with self.bot.db.execute(f"SELECT guild FROM guild WhERE scGuild = 1;") as cur: guilds = await cur.fetchall()
        for r in guilds:
            guild = self.bot.get_guild(r[0])
            leadership = discord.utils.get(guild.roles, name="Leadership_Roles") or await self.role("lsRole",guild)
            if leadership in user.roles: return True
        return False

    async def userSetup(self, user):
        try: 
            await self.bot.db.execute("INSERT INTO members (memberID) VALUES (?);", (user.id),)
            await self.bot.db.commit()
        except Exception: pass

    async def multi(self,guild):
        async with self.bot.db.execute("SELECT xpMulti FROM guild WHERE guild = ?;",(guild,)) as cur: xp = await cur.fetchone()
        return int(xp[0])

    async def levelUp(self,user,ctx):
        async with self.bot.db.execute("SELECT * FROM members WHERE memberID = ?;",(user,)) as cur: level = await cur.fetchone() 
        if level[2] <= level[3] ** 0.25: 
            scb = randint((level[2])*2,((level[2])*3))
            async with self.bot.db.execute("SELECT level FROM members WHERE memberID = ?;",(user,)) as cur: lvl = await cur.fetchone()
            await self.bot.db.execute("UPDATE members SET level = level + 1, scb = scb + ?, xp = xp - ? WHERE memberID = ?;",(scb,lvl[0]**4,user))
            embed = discord.Embed(title=":arrow_up: Level Up :arrow_up:",color=0x2b6a0a)
            embed.set_thumbnail(url=ctx.author.avatar.url)
            embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
            embed.add_field(name="Level",value=level[2]+1)
            embed.add_field(name="Skybucks Gained",value=scb)
            await ctx.channel.send(embed=embed)
            await self.bot.db.commit()
            return True
        return False

    async def sc(self,guild):
        async with self.bot.db.execute("SELECT scGuild FROM guild WHERE guild = ?;",(guild,)) as cur: scguild = await cur.fetchone()
        if not scguild: return False

        if scguild[0] == 1: return True
        else: return False

    @commands.command(name="rank",description="View your level and XP!",aliases=["lvl", "level"])
    async def rank(self, ctx, user : discord.Member = None):
        user = user or ctx.author
        await self.userSetup(user)
        await self.levelUp(ctx.author.id,ctx)
        async with self.bot.db.execute("SELECT level, xp FROM members WHERE memberID = ?;",(user.id,)) as cur: level = await cur.fetchone()
        embed = discord.Embed(title="Rank",color=0x00703C)
        embed.set_thumbnail(url=user.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
        embed.add_field(name="User",value=user,inline=False)
        embed.add_field(name="XP",value=f"{level[1]}/{level[0]**4}",inline=True)
        embed.add_field(name="Level",value=level[0])
        progress = floor(level[1] / level[0]**4)
        a = []
        s = 10
        for i in range(0, progress):
            a.append(":green_square:")
            s-=1
        for i in range(0, s): a.append(":red_square:")
        embed.add_field(name="".join(a), value="_ _",inline=False)
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild: return
        async with self.bot.db.execute("SELECT * FROM bannedWords WHERE guild = ?;",(message.guild.id,)) as cur: bannedWords = await cur.fetchall()
        saidBannedWord = False
        if bannedWords:
            for word in bannedWords: 
                if word[0] in message.content: 
                    await message.send(f"{message.author.mention}, don't say that!")
                    saidBannedWord = True
        if not message.author.bot and not self.message_cooldown.update_rate_limit(message) and await self.sc(message.guild.id) and not saidBannedWord: 
            await self.userSetup(message.author)
            multi = await self.multi(message.guild.id)
            await self.bot.db.execute("UPDATE members SET xp = xp + ? WHERE memberID = ?;",((randint(1,5)*multi),message.author.id)) 
            await self.levelUp(message.author.id,message)

    @commands.command(name="leaderboard",description="View the top rankings of people",aliases=["lb"])
    async def leaderboard(self, ctx):
        async with self.bot.db.execute("SELECT * FROM members ORDER BY level DESC, xp DESC;") as cur: r = await cur.fetchall()
        embed = discord.Embed(title="Leaderboard",color=0x398564)
        rank = 0
        for row in r: 
            try: 
                await self.levelUp(row[0],ctx)
                user = await self.bot.fetch_user(int(row[0]) or await self.bot.get_user(int(row[0])))
                if row[2] != 0 and not user.bot: 
                    place = None
                    rank+=1
                    if rank == 1: place = ":first_place:"
                    elif rank == 2: place = ":second_place:"
                    elif rank == 3: place = ":third_place:"
                    strrank = f"#{rank}"

                    embed.add_field(name=f"**{place or strrank}** {user}",value=f"**Level:** {row[2]} | **XP:** {row[3]}/{row[2]**4}",inline=False)
                if user.bot: await self.bot.db.execute("DELETE FROM members WHERE memberID = ?;",(row[0]))
            except Exception: pass
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
        a = "https://cdn.discordapp.com/icons/921230858311057418/4906a069ad5db4026d9bc068c316c291.webp?size=1024"
        if ctx.guild.icon != None: a = ctx.guild.icon.url
        embed.set_thumbnail(url=a)
        await ctx.send(embed=embed)
    
    @commands.command(name="multi",description="sets the multiplier for xp")
    async def multiplier(self,ctx,multi = None):
        if multi == None: return await ctx.send(f"The multi is currently `{await self.multi(ctx.guild.id)}`.")
        admin = discord.utils.get(ctx.guild.roles,name="Leadership_Roles") or await self.role("lsRole",ctx.guild.id)
        if (admin in ctx.author.roles and await self.sc(ctx.guild.id)) or await self.power(ctx.author):
            await self.bot.db.execute("UPDATE guild SET xpMulti = ? WHERE guild = ?;",(int(multi),ctx.guild.id))
            return await ctx.send(f":white_check_mark: Set the multi to **{multi}**")
        else: await ctx.reply(f"{ctx.author.mention}, you need better permissions!")
    
def setup(bot):
    bot.add_cog(Level(bot))