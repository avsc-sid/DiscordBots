from discord import Embed, User
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

class Zlash(Cog):
    def __init__(self, bot : Bot):
        self.bot = bot

        @cog_ext.cog_slash(name = "actlike", description = "Sends a webhook with the requested users username and avatar.", guild_ids=[726776108351094844])
        async def ActlikeCmd(self, ctx: SlashContext, user: User, content: str):
            webhook = await ctx.channel.create_webhook(name=user.nick or user.name, avatar=await user.avatar_url_as().read())
            await ctx.message.delete()
            await webhook.send(content)
            await webhook.delete()


def setup(bot: Bot):
    bot.add_cog(Zlash(bot))
