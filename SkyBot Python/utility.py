import discord
from discord.ext import commands
from asyncio import sleep
from bot import HelpCMD

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    async def role(self, role, guild):
        async with self.bot.db.execute(f"SELECT {role} FROM guild WHERE guild = ?;",(guild.id,)) as cur: roleId = await cur.fetchone()
        role = discord.utils.get(guild.roles,id=roleId[0])
        return role

    @commands.command(name = "kick", description = "kick members from the server.") 
    async def kick(self, ctx, user : discord.Member, *, reason = "None was specified"):
        try:
            if ctx.author.guild_permissions.kick_members and ctx.author.top_role > user.top_role:
                try: await user.send(f"You got kicked by `{ctx.author}` because `{reason}`")
                except Exception: pass
                await user.kick(reason=reason)
                embed = discord.Embed(name="User Kicked",color=0xf72424)
                embed.add_field(name="User",value=user)
                embed.add_field(name="Kicked By",value=ctx.author.mention)
                embed.add_field(name="Reason",value=reason,inline=False)
                embed.set_thumbnail(url=user.avatar.url)
                embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            else: await ctx.reply("You do not have sufficient permissions.")
        except Exception: await ctx.send(f"{ctx.author.mention}, see `!help kick`")

    @commands.command(name = "ban", description = "bans members from the server.") 
    async def ban(self, ctx, user : discord.Member, *, reason = "None was specified"):
        try: 
            if ctx.author.guild_permissions.ban_members and ctx.author.top_role > user.top_role:
                try: await user.send(f"You got banned by `{ctx.author}` because `{reason}`")
                except Exception: pass
                await user.ban(reason=reason)
                embed = discord.Embed(name="User Banned",color=0xf72424)
                embed.add_field(name="User",value=user)
                embed.add_field(name="Banned By",value=ctx.author.mention)
                embed.add_field(name="Reason",value=reason,inline=False)
                embed.set_thumbnail(url=user.avatar.url)
                embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            else: await ctx.reply("You do not have sufficient permissions or you dont have a higher role than the user.")
        except Exception: await ctx.send(f"{ctx.author.mention}, see `!help ban`")

    @commands.command(name = "mute", description = "Mutes people")
    async def mute(self, ctx, user : discord.Member, * ,reason="None was specified"):
        muted = discord.utils.get(ctx.guild.roles, name = "Muted") or await self.role("mutedRole",ctx.guild)
        try:
            if ctx.author.guild_permissions.kick_members and ctx.author.top_role > user.top_role:
                userRoles = []
                for r in user.roles: 
                    userRoles.append(r.id)
                    await self.bot.db.execute("INSERT INTO muted VALUES (?,?,?,?);",(user.id,ctx.guild.id,r.id,reason))
                try:    await user.send(f"You were muted by `{ctx.author}` because **{reason}**")
                except Exception: pass
                await user.edit(roles=[muted])
                embed = discord.Embed(name="User Muted",color=0xf72424)
                embed.add_field(name="User",value=user)
                embed.add_field(name="Muted By",value=ctx.author.mention)
                embed.add_field(name="Reason",value=reason,inline=False)
                embed.set_thumbnail(url=user.avatar.url)
                embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            else: await ctx.reply("You do not have sufficient permissions.")
        except Exception: await ctx.send(f"{ctx.author.mention}, see `!help mute`")

    @commands.command(name = "unmute", description = "Unmutes people")
    async def unmute(self, ctx, user : discord.Member): 
        try: 
            if ctx.author.guild_permissions.kick_members and ctx.author.top_role > user.top_role:
                async with self.bot.db.execute("SELECT roles, reason FROM muted WHERE id = ? AND  guild = ?;",(user.id,ctx.guild.id)) as cur: fetch = await cur.fetchall()
                membersRoles = []
                reason = "None was specified."
                r = None
                for row in fetch:
                    try: 
                        r = ctx.guild.get_role(int(row[0]))
                        membersRoles.append(r)
                        reason = row[1]
                    except Exception: pass
                await user.edit(roles=membersRoles)
                await self.bot.db.execute("DELETE FROM muted WHERE id = ?;",(user.id,))
                embed = discord.Embed(name="User Unmuted",color=0x0B646D)
                embed.add_field(name="User",value=user)
                embed.add_field(name="Unmuted By",value=ctx.author.mention)
                embed.add_field(name="Reason",value=reason,inline=False)
                embed.set_thumbnail(url=user.avatar.url)
                embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
                try: await user.send(f"You were unmuted by `{ctx.author}`")
                except Exception: pass
                
            else: await ctx.send(f"**{ctx.author}**, you need the permission `Kick Members`!")
        except Exception: await ctx.send(f"{ctx.author.mention}, see `!help unmute`")
    
    @commands.command(name = "purge", description = "Deletes messages")
    async def purge(self, ctx, amount=1):
        try: 
            if ctx.author.guild_permissions.manage_messages and amount >= 0:
                channel = ctx.message.channel
                messages = []
                async for message in channel.history(limit=int(amount) + 1): messages.append(message)
                myMsg = await ctx.send(f"Purged `{amount}` messages successfully!")
                await channel.delete_messages(messages)
                await sleep(1)
                await myMsg.delete()
            else: await ctx.send(f"**{ctx.author.mention}**, you need the `Manage Messages` permission for that, or thats an invalid amount.")
        except Exception: await ctx.send(f"{ctx.author.mention}, see `!help purge`")

    @commands.command(name = "setnickname", description = "changes a users nickname", aliases=["setnick", "sn"])
    async def setnick(self, ctx, user : discord.Member = None, *, nickname = None):
        user = user or ctx.author
        try: 
            if ctx.author.guild_permissions.manage_nicknames and ctx.author.top_role > user.top_role:
                nickName = user.nick
                await user.edit(nick=nickname)
                embed = discord.Embed(title="Changed Nickname",color=0x1CAC78)
                embed.set_thumbnail(url=user.avatar.url)
                embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
                embed.add_field(name="New Nickname",value=user.nick)
                embed.add_field(name="Old Nickname",value=nickName or user.name)
                embed.add_field(name="User",value=user.mention,inline=False)
                await ctx.send(embed=embed)
            else: await ctx.send(f"{ctx.author.mention}, you need better perms!")    
        except Exception: await ctx.send(f"{ctx.author.mention}, see `!help setnick`")

    @commands.command(name="maketag",description="Makes a tag.")
    async def mktag(self,ctx,tagName,*,desc):
        try: await self.bot.db.execute("INSERT INTO tags VALUES (?,?,?);",(tagName,desc,ctx.author.id))
        except Exception: return await ctx.send("Sorry, that tag is already taken.")
        em = discord.Embed(name="Tag Made :white_check_mark:",color=0x5AC18E)
        em.add_field(name=tagName,value=desc)
        em.set_thumbnail(url=ctx.author.avatar.url)
        em.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
        await ctx.send(embed=em)

    @commands.command(name="tag",description="Tag something.")
    async def tag(self,ctx,tag):
        async with self.bot.db.execute("SELECT * FROM tags WHERE name = ?;",(tag,)) as cur: tag = await cur.fetchone()
        user = await self.bot.fetch_user(tag[2]) or await self.bot.get_user(tag[2])
        return await ctx.send(f"{tag[1]}\n\n**-{user}**")
    
        
        

def setup(client):
    client.add_cog(Utility(client))