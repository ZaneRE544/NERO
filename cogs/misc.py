from discord import Embed
from discord.ext.commands import command as jeanne, Cog, has_permissions as perms
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle



class misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne()
    async def invite(self, ctx):
        buttons = [
            create_button(
                style=ButtonStyle.URL,
                label="Bot Invite",
                url="https://discord.com/api/oauth2/authorize?client_id=831993597166747679&permissions=2550197270&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D831993597166747679%26scope%3Dbot&scope=bot%20applications.commands"
            ),
            create_button(
                style=ButtonStyle.URL,
                label="Top.gg",
                url="https://top.gg/bot/831993597166747679"
            ),
            create_button(
                style=ButtonStyle.URL,
                label="DiscordBots",
                url="https://discord.bots.gg/bots/831993597166747679"
            ),
            create_button(
                style=ButtonStyle.URL,
                label="HAZE",
                url="https://discord.gg/VVxGUmqQhF"
            ),]

        action_row=create_actionrow(*buttons)

        embed = Embed(
            title="Invite me!",
            description="Click on one of these buttons to invite me to you server or join my creator's server",
            color=0x00bfff)

        await ctx.send(embed=embed, components=[action_row])

    @jeanne()
    @perms(administrator=True)
    async def say(self, ctx, *, text):
        message = ctx.message
        await message.delete()
        await ctx.send(text)

    @jeanne(name='saye')
    @perms(administrator=True)
    async def sayembed(self, ctx, *, text):
        message = ctx.message
        say = Embed(description=f"{text}", color=0xADD8E6)
        await message.delete()
        await ctx.send(embed=say)


def setup(bot):
    bot.add_cog(misc(bot))
