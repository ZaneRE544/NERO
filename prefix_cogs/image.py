from functions import BetaTest, Botban, Command
from discord import Color, Embed, Interaction
from discord.ext.commands import Cog, Bot, Context
import discord.ext.commands as Jeanne
from config import kitsune_nekoslife, neko_purrbot
from requests import get
from assets.images import (
    get_jeanne_pic,
    get_medusa_pic,
    get_saber_pic,
    get_wallpaper_pic,
    safebooru_pic,
)


class images(Cog, name="Images"):
    def __init__(self, bot):
        self.bot = bot

    @Jeanne.command(description="Get a kitsune image")
    async def kitsune(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user:
            return
        check = await BetaTest(self.bot).check(ctx.author)

        if check == True:
            if Command(ctx.guild).check_disabled(self.kitsune.qualified_name):
                await ctx.send(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return

            await ctx.defer()

            kistune_api = get(kitsune_nekoslife).json()
            kitsune = Embed(color=Color.random())
            kitsune.set_footer(
                text="Fetched from nekos.life • Credits must go to the artist"
            )
            kitsune.set_image(url=kistune_api["url"])
            await ctx.send(embed=kitsune)

    @Jeanne.command(description="Need a wallpaper for your PC or phone?")
    async def wallpaper(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.wallpaper.qualified_name):
            await ctx.send(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.defer()
        embed, file = get_wallpaper_pic()
        await ctx.send(embed=embed, file=file)

    @Jeanne.command(description="Get a Jeanne d'Arc image")
    async def jeanne(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.jeanne.qualified_name):
            await ctx.send(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.defer()
        embed, file = get_jeanne_pic()
        await ctx.send(embed=embed, file=file)

    @Jeanne.command(description="Get a Saber image")
    async def saber(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.saber.qualified_name):
            await ctx.send(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.defer()
        file, embed = get_saber_pic()
        await ctx.send(file=file, embed=embed)

    @Jeanne.command(description="Get a neko image")
    async def neko(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.neko.qualified_name):
            await ctx.send(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.defer()

        neko_api = get(neko_purrbot).json()
        neko = Embed(color=Color.random())
        neko.set_image(url=neko_api["link"])
        neko.set_footer(
            text="Fetched from PurrBot.site • Credits must go to the artist"
        )
        await ctx.send(embed=neko)

    @Jeanne.command(description="Get a Medusa (Fate) image")
    async def medusa(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.medusa.qualified_name):
            await ctx.send(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.defer()
        embed, file = get_medusa_pic()
        await ctx.send(embed=embed, file=file)

    @Jeanne.command(description="Get an image from Safebooru")
    async def safebooru(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.safebooru.qualified_name):
            await ctx.send(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.defer()
        embed = Embed(color=Color.random())
        embed.set_image(url=safebooru_pic())
        embed.set_footer(text="Fetched from Safebooru • Credits must go to the artist")
        await ctx.send(embed=embed)


async def setup(bot: Bot):
    await bot.add_cog(images(bot))