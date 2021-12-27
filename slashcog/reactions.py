from discord import Member, Embed
from discord.ext.commands import Cog
from requests import get
from assets.needed import poke_nekoslife, tickle_nekoslife, baka_nekoslife, feed_nekoslife, slap_nekoslife, smug_nekoslife, hug_nekoslife, pat_nekoslife, kiss_nekoslife
from discord_slash.cog_ext import cog_slash as jeanne_slash

class reactions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne_slash(description="Hug someone or yourself")
    async def hug(self, ctx, member : Member = None):
            hug_api = get(hug_nekoslife).json()
            if member == None:
                msg=f"*Hugging {ctx.author.mention}*"
            else:
                msg=f"*{ctx.author.mention} hugged {member.mention}*"
            hug = Embed(color=0xFFC0CB)
            hug.set_footer(text="Fetched from nekos.life")
            hug.set_image(url=hug_api["url"])
            await ctx.send(msg, embed=hug)

    @jeanne_slash(description="Slap someone or yourself")
    async def slap(self, ctx, member: Member = None):
        slap_api = get(slap_nekoslife).json()

        slap = Embed(color=0xFFC0CB)
        slap.set_footer(text="Fetched from nekos.life")
        slap.set_image(url=slap_api["url"])
        if member == None:
                msg=f"*Slapping {ctx.author.mention}*"
        else:
                msg=f"*{ctx.author.mention} slapped {member.mention}*"
        await ctx.send(msg, embed=slap)

    @jeanne_slash(description="Show a smuggy look")
    async def smug(self, ctx):
        smug_api = get(smug_nekoslife).json()

        smug = Embed(color=0xFFC0CB)
        smug.set_footer(text="Fetched from nekos.life")
        smug.set_image(url=smug_api["url"])
        await ctx.send(f"*{ctx.author.mention} is smugging*", embed=smug) 

    @jeanne_slash(description="Poke someone or yourself")
    async def poke(self, ctx, member: Member = None):
        poke_api = get(poke_nekoslife).json()
        poke = Embed(color=0xFFC0CB)
        poke.set_footer(text="Fetched from nekos.life")
        poke.set_image(url=poke_api["url"])
        if member == None:
                msg=f"*Poking {ctx.author.mention}*"
        else:
                msg=f"*{ctx.author.mention} poked {member.mention}*"
        await ctx.send(msg, embed=poke)

    @jeanne_slash(description="Pat someone or yourself")
    async def pat(self, ctx, member: Member = None):
        pat_api = get(pat_nekoslife).json()
        pat = Embed(color=0xFFC0CB)
        pat.set_footer(text="Fetched from nekos.life")
        pat.set_image(url=pat_api["url"])
        if member == None:
                msg=f"*Patting {ctx.author.mention}*"
        else:
                msg=f"*{ctx.author.mention} patted {member.mention}*"
        await ctx.send(msg, embed=pat)

    @jeanne_slash(description="Kiss someone or yourself")
    async def kiss(self, ctx, member: Member = None):
            kiss_api = get(kiss_nekoslife).json()
            if member == None:
                msg=f"*Kissing {ctx.author.mention}*"
            else:
                msg=f"*{ctx.author.mention} kissed {member.mention}*"
            kiss = Embed(color=0xFFC0CB)
            kiss.set_footer(text="Fetched from nekos.life")
            kiss.set_image(url=kiss_api["url"])
            await ctx.send(msg, embed=kiss)

    @jeanne_slash(description="Tickle someone or yourself")
    async def tickle(self, ctx, member: Member = None):
            tickle_api = get(tickle_nekoslife).json()
            if member == None:
                msg=f"*Tickling {ctx.author.mention}*"
            else:
                msg=f"*{ctx.author.mention} tickled {member.mention}*"
            tickle = Embed(color=0xFFC0CB)
            tickle.set_footer(text="Fetched from nekos.life")
            tickle.set_image(url=tickle_api["url"])
            await ctx.send(msg, embed=tickle)

    @jeanne_slash(description="Call someone or yourself a baka!")
    async def baka(self, ctx, member: Member = None):
            baka_api = get(baka_nekoslife).json()
            if member == None:
                msg=f"*{ctx.author.mention}, you are a baka!*"
            else:
                msg=f"*{member.mention}, {ctx.author.mention} called you a baka!*"
            baka = Embed(color=0xFFC0CB)
            baka.set_footer(text="Fetched from nekos.life")
            baka.set_image(url=baka_api["url"])
            await ctx.send(msg, embed=baka)

    @jeanne_slash(description="Feed someone or yourself")
    async def feed(self, ctx, *, member: Member = None):
        feed_api = get(feed_nekoslife).json()
        if member == None:
            msg = f"*Feeding {ctx.author.mention}*"
        else:
            msg = f"*{ctx.author.mention} fed {member.mention}*"
        feed = Embed(color=0xFFC0CB)
        feed.set_footer(text="Fetched from nekos.life")
        feed.set_image(url=feed_api["url"])
        await ctx.send(msg, embed=feed)


def setup(bot):
    bot.add_cog(reactions(bot))
