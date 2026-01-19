from discord.ext import commands
import wavelink
import discord
from wavelink.ext import spotify

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.node())
        self.queue = {}


    async def node(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot,host='lava.link',port=80,password='m',spotify_client=spotify.SpotifyClient(client_id="id", client_secret="secret"))

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        if not self.queue.get(player.guild.id): self.queue[player.guild.id] = {}
        if not self.queue[player.guild.id].get("queue"): self.queue[player.guild.id]["queue"] = "none"

        if self.queue[player.guild.id]["queue"] == "queue": player.queue.put(track)
        elif self.queue[player.guild.id]["queue"] == "current": player.queue.put_at_front(track)

        if player.queue.is_empty: return await player.stop()

        if self.queue[player.guild.id].get("channel"):
            channel = self.bot.get_channel(self.queue[player.guild.id]["channel"])
            if reason == "STOPPED": await channel.send(f"Skipped {track.title}!")
            else: await channel.send(f":white_check_mark: Finished playing {track.title}!")

        next_song = player.queue.get()
        await player.play(next_song)


    @commands.command(name = "join", description = "Joins vc.", aliases=["j","connect"])
    async def join(self, ctx):
        if ctx.author.voice == None: await ctx.send("You aren't in a voice channel!")
        else:
            player = wavelink.NodePool.get_node().get_player(ctx.guild)
            if not player:
                await ctx.author.voice.channel.connect(cls=wavelink.Player)
                if not self.queue.get(ctx.guild.id): self.queue[ctx.guild.id] = {}
                self.queue[ctx.guild.id]["channel"] = ctx.channel.id
                await ctx.send(f"Successfully connected to `{ctx.author.voice.channel}` and bound to `{ctx.channel.name}`!")
            else:
                await ctx.voice_client.move_to(ctx.author.voice.channel)
                await ctx.send(f"Successfully moved to `{ctx.author.voice.channel}`!")

    @commands.command(name = "disconnect", description = "disconnects SkyBot from vc", aliases=["disc"])
    async def disconnect(self, ctx):
        if ctx.voice_client:
            if not ctx.author.voice: return await ctx.send("You aren't in VC.")
            await ctx.me.move_to(None)
            await ctx.send(f"Disconnected from `{ctx.author.voice.channel}`")
            player = wavelink.NodePool.get_node().get_player(ctx.guild)
            await player.stop()
        else: return await ctx.send(f"{ctx.author.mention}, I'm not connected to a vc!")

    @commands.command(name="play", description="play audio")
    async def play(self, ctx, *, query = None):
        if not ctx.voice_client: await ctx.invoke(self.join)
        player = wavelink.NodePool.get_node().get_player(ctx.guild)
        if player.queue:
            if player.queue.is_full: return await ctx.send("The queue is full.")
        if not query:
            await player.set_pause(pause=False)
            return await ctx.send("Resuming...")

        if not self.queue.get(ctx.guild.id): self.queue[ctx.guild.id] = {}
        self.queue[ctx.guild.id]["channel"] = ctx.channel.id
        self.queue[ctx.guild.id]["queue"] = "none"

        decoded = spotify.decode_url(query)
        if not decoded in [None,spotify.SpotifySearchType.unusable]:
            msg = await ctx.send(f":mag: Searching Spotify for `{query}`...")
            if "open.spotify.com/playlist" in query:
                async for track in spotify.SpotifyTrack.iterator(query=query, type=spotify.SpotifySearchType.playlist): player.queue.put(track)
                return await msg.edit(content=":thumbsup: Added all songs to the queue.")
            else:
                track = await spotify.SpotifyTrack.search(query=query, return_first=True)
        elif "soundcloud.com/" in query:
            msg = await ctx.send(f":mag: Searching SoundCloud for `{query}`...")
            if "/sets/" in query:
                tracks = await wavelink.SoundCloudTrack.search(query=query)
                async for track in tracks: player.queue.put(track)
                return await ctx.send("Added all songs to the queue.")
            else: track = await wavelink.SoundCloudTrack.search(query=query,return_first=True)

        else:
            msg = await ctx.send(f":mag: Searching YouTube for `{query}`...")
            try:
                track = await wavelink.YouTubeTrack.search(query=query, return_first=True)
                if not track: return await msg.edit(content=f"{ctx.author.mention}, I could not find any commands with this query.")
            except Exception: return await ctx.send(f"Timeout error. {ctx.author.mention} run the command again.")

        await msg.edit(content=f":thumbsup: Added `{str(track.title)}` to the queue.")
        if ctx.voice_client.is_playing(): return player.queue.put(track)
        return await player.play(track)

    @commands.command(name="skip",description="skips the current song!")
    async def skip(self,ctx):
        if not ctx.voice_client: await ctx.invoke(self.join)
        player = wavelink.NodePool.get_node().get_player(ctx.guild)
        await player.stop()

    @commands.command(name="seek",description="seeks for the location you specified (in seconds). Does not support hours.")
    async def seek(self,ctx,time):
        if not ctx.voice_client: await ctx.invoke(self.join)
        time = time.split(":")
        player = wavelink.NodePool.get_node().get_player(ctx.guild)
        if player.queue.is_empty: return await ctx.send("The queue is empty.")
        if type(time) == list:
            minutes = int(time[-2])*60000
            seconds = int(time[-1])*1000
            await player.seek(position=minutes+seconds)
        else: await player.seek(position=time*1000)
        await ctx.send(f"Changed the position to `{time}` :thumbsup:")

    @commands.command(name="pause",description="pauses the song")
    async def pause(self,ctx):
        if not ctx.voice_client: await ctx.invoke(self.join)
        player = wavelink.NodePool.get_node().get_player(ctx.guild)
        if player.queue.is_empty: return await ctx.send("The queue is empty.")
        await ctx.voice_client.pause()
        await ctx.send(f":thumbsup: Paused the song!")

    @commands.command(name="volume",description="sets the volume to a random integer between 1 and 100")
    async def volume(self,ctx,volume):
        if not ctx.voice_client: await ctx.invoke(self.join)
        player = wavelink.NodePool.get_node().get_player(ctx.guild)
        if player.queue.is_empty: return await ctx.send("The queue is empty.")
        await player.set_volume(volume=volume*10)
        await ctx.send(f"Set the volume to **{volume}** :thumbsup:")

    @commands.command(name="queue",description="shows the queue")
    async def queue(self,ctx):
        if not ctx.voice_client: await ctx.invoke(self.join)
        player = wavelink.NodePool.get_node().get_player(ctx.guild)
        try:
            embed = discord.Embed(name="Up Next",color=0x1B2BA5)

            embed.add_field(name=f"Now Playing: {player.track.title}",value=f"Position: {player.position}/{player.track.length} seconds")

            embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar.url)
            songs=""
            for song in player.queue: songs = songs + str(song.title) + "\n"
            embed.add_field(name="Songs",value=songs or "(Empty)")
            return await ctx.send(embed=embed)
        except: return await ctx.send("The queue is empty.")

    @commands.command(name="loop",description="sets the loop to the loop of your choice")
    async def loop(self,ctx,type=None):
        if not ctx.voice_client: await ctx.invoke(self.join)
        player = wavelink.NodePool.get_node().get_player(ctx.guild)
        if type == None:
            if not self.queue.get(player.guild.id): loop = self.queue[player.guild.id]
            else:
                loop = "none"
                if not self.queue.get(player.guild.id): self.queue[player.guild.id] = {"queue": "none"}
            return await ctx.send(f"The current queue type is `{loop}`.")

        if not type.lower() in ["queue","current","none"]: return await ctx.send("The options are `queue`, `none` and `current`.")
        if not self.queue[ctx.guild.id]: self.queue[ctx.guild.id] = {}
        self.queue[ctx.guild.id]["queue"] = type
        await ctx.send(f":thumbsup: Set the loop to `{type}`!")

    @commands.command(name="stop",description="stops all songs")
    async def stop(self,ctx):
        player = wavelink.NodePool.get_node().get_player(ctx.guild)
        if not player.queue.is_empty: player.queue.clear()
        await player.stop()
        await ctx.invoke(self.disconnect)
        return await ctx.send("Stopped the current song and cleared the queue.")

def setup(bot):
    bot.add_cog(Music(bot))
