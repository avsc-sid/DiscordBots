from discord.ext import commands
import discord
import random
from random import choice
from requests import get
from asyncio import sleep
from aiohttp import ClientSession

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "echo", description = "copies message and prints", aliases = ["cc","copycat","me", "mimic"])
    async def echo(self, ctx, *, args):
        await ctx.send(f' {args} **-{ctx.author}**')


    @commands.command(name = "choose", description = "chooses a random thing", aliases = ["randomchoice", "rc", "choice"])
    async def choose(self, ctx, *, choices):
        if choices.__contains__(','): m = ','
        else: m = ' '
        e = choices.split(m)
        await ctx.send(f"I choose... `{choice(e)}`")


    @commands.command(name = "yomama", description = "sends random yo mama joke", aliases = ["ym", "yopapa"])
    async def yomama(self, ctx):
        res  = get("https://api.yomomma.info/")
        res_json = res.json()
        joke = res_json["joke"]
        await ctx.reply(joke)
    
    @commands.command(name = "8ball", description = "The Magic 8ball (try this: !8ball [A random question])")
    async def eightBall(self, ctx, *, question):
        responses = ["It is certain.", "Without a doubt.", "You may rely on it.", "Yes, definitely.", "It is decidedly so.", "As I see it, yes.", "Most likely.", "Yes.", "Outlook good.", "Signs point to yes.", "Reply hazy try again.", "Better not tell you now.", "Ask again later.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "Outlook not so good.", "My sources say no.", "Very doubtful.", "My reply is no."]
        await ctx.reply(f"`{question}?` {random.choice(responses)}")

    #dice roll(badly coded by darkfang), no idea if it works
    @commands.command(name = "rolldice", description = "rolls a random number of your choice ", aliases = ["rd", "roll"])
    async def rolldice(self, ctx, faces=6, diceAmt=1, addamt=0):
        rollresult=[random.randint(1, faces) for _ in range(diceAmt)]
        rollresult=sum(rollresult)+addamt
        em = discord.Embed(title = "Roll Dice",color=choice(self.bot.colorList))
        em.add_field(name = "Rolled number", value = f"{ctx.author.mention} rolled {rollresult} dice!", inline=False)
        em.add_field(name = "Dice Amount", value = diceAmt, inline=True)
        em.add_field(name = "Sides", value = faces, inline=True)
        em.add_field(name = "Added Amount", value=addamt, inline=True)
        em.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
        em.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.reply(embed=em)
        
    #coin flip, flips a coin
    @commands.command(name = "coinflip", description = "flips a coin", aliases = ["cf", "flipcoin"])
    async def coinflip(self, ctx):
        flipresult = random.choice(['heads', 'tails'])
        em = discord.Embed(title = "Coin Flip", color=choice(self.bot.colorList))
        em.add_field(name=f"{ctx.author}'s flip", value= f"{ctx.author.mention} flipped {flipresult}!", inline=False)
        em.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
        em.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.reply(embed=em)

    @commands.command(name = "numbergame", description = "play a game where you guess the number", aliases = ["ng", "guess","guessinggame","numgame"])
    async def numbergame(self, ctx): 
        mystnum=random.randint(1,100)
        guess=-1
        gc=0
        players = {}
        while guess!=mystnum:
            await ctx.reply("what number do you guess?")
            msg = await self.bot.wait_for("message", check=lambda msg: msg.channel == ctx.channel and msg.content.isnumeric())
            if not str(msg.author) in players: players[str(msg.author)] = 1
            players[str(msg.author)]+=1

            guess=int(msg.content)
            if int(guess) > mystnum: 
                gc+=1
                await ctx.reply("The number you guessed was too high, guess lower")
            elif int(guess) < mystnum: 
                gc+=1
                await ctx.reply("The number you guessed was too low, guess higher")
            else: 
                embed = discord.Embed(title="Number Game Results",color=choice(self.bot.colorList))
                ppl = ""
                guesses = ""
                for user, guess in players.items(): 
                    ppl = ppl + f"{user}\n"
                    guesses = guesses + f"{guess}\n"
                embed.add_field(name="Guesses",value=guesses)
                embed.add_field(name="User",value=ppl)
                embed.set_thumbnail(url=ctx.author.avatar.url)
                embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
                return await ctx.reply(embed=embed)

    @commands.command(name = "sendembed", description = "Sends an embed of your desire!", aliases = ["se", "embed"])
    async def sendembed(self, ctx):
        em = discord.Embed(title = "A Title", color=choice(self.bot.colorList), description="A Description")
        await ctx.reply("What's the title of the embed? Enter `quit` at any point to quit the process.")

        def c(m):
            return m.author == ctx.author and m.channel == ctx.channel

        newTitle = await self.bot.wait_for("message", check=c)
        if newTitle.content == "quit": return await ctx.send("You have quit the process.")

        await ctx.reply("What's the description of the embed?")
        newDesc = await self.bot.wait_for("message", check=c)
        if newDesc.content == "quit": return await ctx.send("You have quit the process.")

        await ctx.reply("What's the footer of the embed?")
        newFooter = await self.bot.wait_for("message", check=c)
        if newFooter.content == "quit": return await ctx.send("You have quit the process.")

        em = discord.Embed(title = newTitle.content, description = newDesc.content, color=choice(self.bot.colorList))
        em.set_footer(text=newFooter.content, icon_url=ctx.author.avatar.url)
        deletecount = 9

        await ctx.reply('How many fields do you want')
        fieldnum = await self.bot.wait_for("message", check=c)
        if newTitle.content == "quit": return await ctx.send("You have quit the process.")
        if not fieldnum.content.isnumeric(): return await ctx.reply("Thats not a valid number.")

        for i in range (0, int(fieldnum.content)):
            await ctx.reply(f"What's the title for field {i + 1}?")
            title = await self.bot.wait_for("message", check=c)
            if newTitle.content == "quit": return await ctx.send("You have quit the process.")

            await ctx.reply(f"What's the description for field {i + 1}")
            desc = await self.bot.wait_for("message", check=c)
            if newTitle.content == "quit": return await ctx.send("You have quit the process.")

            await ctx.reply(f"Do you want field {i + 1} to be inline? (T)rue or (F)alse")
            inline = await self.bot.wait_for("message", check=c)
            if newTitle.content == "quit": return await ctx.send("You have quit the process.")

            if str(inline.content).lower() in ('true', 't', 'yes', 'y'): inline=True
            elif str(inline.content).lower() in ('false', 'f', 'no', 'no'): inline=False
            else: break

            em.add_field(name = (title.content), value = (desc.content), inline=bool(inline))
            deletecount+=6
        await ctx.message.channel.purge(limit=deletecount, check=lambda c: c.author == ctx.author or c.author == self.bot.user and not c.content.startswith("!sendembed"))
        await ctx.send(embed=em)

        
    @commands.command(name = "actlike", description = "Sends a webhook with the requested users username and avatar.", aliases = ["al","impersonate"])
    async def actlike(self, ctx, user : discord.Member = None,  *, content="Hi!"):
        webhook = await ctx.channel.create_webhook(name=user.nick or user.name, avatar=await user.avatar.read())
        await ctx.message.delete()
        await webhook.send(content)
        await webhook.delete()

    @commands.command(name = "rps", description = "play rock paper scissors", aliases = ["rockpaperscissors", "rockpaperscissor"])
    async def rockpaperscissors(self,ctx):
        choices=['r','p','s']
        botc=random.choice(choices)
        await ctx.reply('what do you choose (r)ock (p)aper or (s)cissors')
        msg = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel and
        msg.content.lower() in ['r', 'p', 's', 'rock', 'paper', 'scissors'])
        if msg.content.lower() in ("r", "rock"):
            if botc==('r'):
                await ctx.reply("Skybot chose rock, You tied")
            elif botc==('p'):
                await ctx.reply("Skybot chose paper, You lost")
            else:
                await ctx.reply("Skybot chose scissors, You won")
        elif msg.content.lower() in ("p", "paper"):
            if botc==('r'):
                await ctx.reply("Skybot chose rock, You won")
            elif botc==('p'):
                await ctx.reply("Skybot chose paper, You tied")
            else:
                await ctx.reply("Skybot chose scissors, You lost")
        else:
            if botc==('r'):
                await ctx.reply("Skybot chose rock, You lost")
            elif botc==('p'):
                await ctx.reply("Skybot chose paper, You won")
            else:
                await ctx.reply("Skybot chose scissors, You tied")

    @commands.command(name="addjoke",description="Add a joke to the list of jokes!",aliases=["createjoke","makejoke"])
    async def addjoke(self, ctx, *, joke : str):
        try: await self.bot.db.execute("INSERT INTO jokes VALUES (?,?);",(int(ctx.author.id),joke))
        except: return await ctx.reply("That joke is already taken.")
        embed = discord.Embed(title="Added Joke :thumbsup:",color=0x5ac18e)
        embed.add_field(name="Joke",value=joke)
        embed.add_field(name="Author",value=ctx.author.mention)
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)
        await self.bot.db.commit()

    @commands.command(name="joke",description="choose a random joke from the list of jokes",aliases=["sayjoke"])
    async def joke(self, ctx, user : discord.Member = None):
        if user != None: 
            async with self.bot.db.execute("SELECT * FROM jokes WHERE id = ? ORDER BY RANDOM() LIMIT 1;",(user.id,)) as cur: joke = await cur.fetchone()
            person = None
        else:
            async with self.bot.db.execute("SELECT * FROM jokes ORDER BY RANDOM() LIMIT 1;") as cur: joke = await cur.fetchone()
            if not joke: return await ctx.send("The user you specified has no jokes.")
            person = await self.bot.fetch_user(joke[0]) or await self.bot.get_user(joke[0])
        if not joke: return await ctx.reply("The user you specified has no jokes.")
        embed = discord.Embed(title="Joke",color=choice(self.bot.colorList))
        if hasattr(user, "avatar.url"): embed.set_thumbnail(url=user.avatar.url)
        else: embed.set_thumbnail(url=person.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
        embed.add_field(name="Joke",value=f"\"{joke[1]}\"")
        embed.add_field(name="Author",value=user or person)
        await ctx.reply(embed=embed)

    @commands.command(name="spam", description="Sends one message repeatedly up to 10 times! It has a pretty high cooldown though...", aliases=["sapm"])
    @commands.cooldown(1, 7200.0, commands.BucketType.user)
    async def spam(self, ctx, number : str = None, *, msg : str = None):
        try:
            if number == None:
                return await ctx.reply("Please enter the number of messages I should spam.")
            try: int(number)
            except: return await ctx.reply("Your first argument must be an integer (up to 10!).")
            number = int(number)
            if number > 10:
                return await ctx.reply("You cannot enter a number higher than 10.")
            if msg == None or len(msg) == 0:
                return await ctx.reply("Please enter something for me to spam.")
            while number > 0:
                await ctx.send(msg + f"           ({number-1} messages left)")
                number -= 1
                await sleep(.5)
        except discord.errors.HTTPException:
            await ctx.send("Please shorten your message a bit.")
    
    @commands.command(name="meme",description="Sends a meme.")
    async def meme(self,ctx,*,category="hot"):      
        async with ClientSession() as cs:
            async with cs.get(f'https://www.reddit.com/r/memes/new.json?sort={category}') as r: res = await r.json()
        meme = res["data"]["children"][random.randint(0,10)]["data"]
        embed = discord.Embed(title=meme["title"], description=meme["author"],color=random.choice(self.bot.colorList))      
        
        embed.set_image(url=meme['url'])
        embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Fun(client))