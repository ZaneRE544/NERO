import discord
import random
from discord.ext import commands
from discord.ext.commands.converter import clean_content
from discord.ext.commands.errors import CommandOnCooldown, NSFWChannelRequired
import requests


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['8ball', 'test', '8b'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _8ball(self, ctx, *, question=None):
        responses = [
            'It is certain.', 'It is decidedly so.', 'Without a doubt.',
            'Yes – definitely.', 'You may rely on it.', 'As I see it, yes.',
            'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
            'Reply hazy, try again.', 'Ask again later.',
            'Better not tell you now.', 'Cannot predict now.',
            'Concentrate and ask again.', 'Dont count on it.', 'My reply is no.',
            'My sources say no.', 'Outlook not so good.', 'Very doubtful.'
        ]
        embed = discord.Embed(color=0x0000FF)
        embed.add_field(name="Question:", value=f'{question}', inline=False)
        embed.add_field(
            name="Answer:", value=f'{random.choice(responses)}', inline=False)
        await ctx.send(embed=embed)

        if question==None:
            noquestion = discord.Embed(
                description="Please add a question")
        await ctx.send(embed=noquestion)

    @commands.command(aliases=['rd', 'dice'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rolldice(self, ctx):
        embed = discord.Embed(color=0x0000FF)
        embed.add_field(name="Dice Rolled", value="You rolled a {}!".format(
            random.randint(1, 6)), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def combine(self, ctx, name1: clean_content, name2: clean_content):
        name1letters = name1[:round(len(name1) / 2)]
        name2letters = name2[round(len(name2) / 2):]
        ship = "".join([name1letters, name2letters])
        emb = (discord.Embed(color=0x36393e, description=f"{ship}"))
        emb.set_author(name=f"{name1} + {name2}")
        await ctx.send(embed=emb)

    @commands.command(aliases=['coinflip', 'headsortails', 'piece'])
    async def flip(self, ctx):
        await ctx.send(embed=discord.Embed(color=0x0000FF,
                                           description=f"`{random.choice(['Heads', 'Tails'])}`"))

    @commands.command(aliases=['h'])
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hentai(self, ctx, *, tag=None):
        badtags=["loli", "shota", "cub", "scat", "shit", "vore", "ugly_bastard", "gore", "guro"]
        if tag == None:
            tag = ""
        elif any(word in tag.lower() for word in badtags):
            blacklisted_tags = discord.Embed(description="This tag is currently blacklisted")
            await ctx.send(embed=blacklisted_tags)
        else:
            yandere_api = random.choice(requests.get(
                        f"https://yande.re/post.json?tags=rating:explicit-loli-shota-cub-scat-ugly_bastard-vore-guro-child-urine{tag}").json())
            yandere = discord.Embed(color=0xFFC0CB)
            yandere.set_image(url=yandere_api["file_url"])
            yandere.set_footer(text="Fetched from Yande.re")

            await ctx.send(embed=yandere)

        if IndexError:
            print(f"{tag} is not found in Yande.re API")  # this prevents the bot to fall apart whenever a tag is not found for some reason

    @commands.command(aliases=["pick"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def choose(self, ctx, *choices: str):
        if len(choices) > 1:
            choose = discord.Embed(
                description=f"I chose **{random.choice(choices)}**")
            await ctx.send(embed=choose)

        elif len(choices) == 1:
            nochoices = discord.Embed(
                description="Please add more than 1 choices")
        await ctx.send(embed=nochoices)



def setup(bot):
    bot.add_cog(fun(bot))
