from asyncio import TimeoutError
from random import choice, randint
from glob import glob
from nextcord import Embed, File
from nextcord.ext.commands import command as jeanne, Cog, BucketType, cooldown
from nextcord.ext.commands.converter import clean_content
from assets.needed import eight_ball_answers, correct_answer, wrong_answer_or_timeout


class fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne(aliases=['8ball', '8b'])
    @cooldown(1, 5, BucketType.user)
    async def _8ball(self, ctx, *, question=None):
        if not question:
            noquestion = Embed(
                description="Please add a question")
            await ctx.send(embed=noquestion)
        else:
            embed = Embed(color=0x0000FF)
            embed.add_field(name="Question:", value=f'{question}', inline=False)
            embed.add_field(
                name="Answer:", value=f'{choice(eight_ball_answers)}', inline=False)
            await ctx.send(embed=embed)

    @jeanne(aliases=['rd', 'dice'])
    @cooldown(1, 5, BucketType.user)
    async def rolldice(self, ctx):
        rolled=randint(1,6)
        embed = Embed(color=0x0000FF)
        embed.add_field(name="Dice Rolled", value=f"You rolled a **{rolled}**!", inline=False)
        await ctx.send(embed=embed)

    @jeanne()
    @cooldown(1, 5, BucketType.user)
    async def combine(self, ctx, name1: clean_content, name2: clean_content):
        option_name1letters = name1[:round(len(name1) / 2)]
        option_name2letters = name2[round(len(name2) / 2):]
        combine1 = "".join([option_name1letters, option_name2letters])
        option2_name1letters = name1[round(len(name1) / 2):]
        option2_name2letters = name2[:round(len(name2) / 2)]
        combine2 = "".join([option2_name1letters, option2_name2letters])
        emb = Embed(
            description=f"**1st combine word:** {combine1}\n**2nd combined word:** {combine2}", color=0x0000FF)
        emb.set_author(name=f"{name1} + {name2}")
        await ctx.send(embed=emb)

    @jeanne(aliases=['coinflip', 'headsortails', 'piece'])
    async def flip(self, ctx):
        await ctx.send(embed=Embed(color=0x0000FF,
                                           description=f"`{choice(['Heads', 'Tails'])}`"))

    @jeanne()
    @cooldown(1, 5, BucketType.user)
    async def reverse(self, ctx, *, text):
        await ctx.delete()
        await ctx.send(text[::-1])

    @jeanne()
    @cooldown(1, 5, BucketType.user)
    async def guess(self, ctx):
        guessit = Embed(
            description="Guess my number!\nYou have 5 seconds to guess it", color=0x00FFFF)
        await ctx.send(embed=guessit)
        if ctx.author.id == self.bot.user.id:
            return

        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()

        answer = randint(1, 10)

        try:
            guess = await self.bot.wait_for("message", check=is_correct, timeout=5.0)
        except TimeoutError:
            timeout = Embed(
                description=f"Sorry but you took too long. It was {answer}", color=0xFF0000)
            timeout.set_thumbnail(url=wrong_answer_or_timeout)
            return await ctx.send(embed=timeout)

        if int(guess.content) == answer:
            correct = Embed(description="YES!", color=0x008000)
            correct.set_image(url=correct_answer)
            await ctx.send(embed=correct)
        else:
            wrong = Embed(
                description=f"Wrong answer. It was {answer}", color=0xFF0000)
            wrong.set_thumbnail(url=wrong_answer_or_timeout)
            await ctx.send(embed=wrong)

    @jeanne()
    @cooldown(1, 5, BucketType.user)
    async def animeme(self, ctx):
            file_path_type = ["./Media/Animemes/*.mp4", "./Media/Animemes/*.jpg"]
            animemes = glob(choice(file_path_type))
            random_animeme = choice(animemes)
            file = File(random_animeme)
            animeme = Embed(color=0x0000FF)
            animeme.set_footer(text="Powered by JeanneBot")
            await ctx.send(file=file, embed=animeme)

def setup(bot):
    bot.add_cog(fun(bot))
