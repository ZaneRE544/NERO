from discord.ext.commands import Cog, Bot, GroupCog
from discord import (
    Color,
    Embed,
    File,
    Interaction,
    Member,
    app_commands as Jeanne,
    Message,
)
from config import TOPGG
from functions import (
    Botban,
    Command,
    Inventory,
    Levelling,
)
from typing import Optional
from assets.generators.profile_card import Profile
from collections import OrderedDict
from json import loads
from topgg import DBLClient


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


class Rank_Group(GroupCog, name="rank"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @Jeanne.command(
        name="global", description="Check the users with the most XP globally"
    )
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    async def _global(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self._global.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        embed = Embed(color=Color.random())
        embed.set_author(name="Global XP Leaderboard")

        leaderboard = Levelling().get_global_rank

        if leaderboard == None:
            embed.description = "No global leaderboard provided"
            await ctx.followup.send(embed=embed)
            return

        r = 0
        for i in leaderboard:
            p = await self.bot.fetch_user(i[0])
            exp = i[3]
            r += 1
            embed.add_field(name=f"`{r}.` {p}", value=f"`{exp}XP`", inline=True)

        await ctx.followup.send(embed=embed)

    @Jeanne.command(description="Check the users with the most XP in the server")
    @Jeanne.checks.cooldown(1, 60, key=lambda i: (i.user.id))
    async def server(self, ctx: Interaction):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.server.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        await ctx.response.defer()
        embed = Embed(color=Color.random())
        embed.set_author(name="Server XP Leaderboard")

        leaderboard = Levelling(server=ctx.guild).get_server_rank

        if leaderboard == None:
            embed.description = "No server leaderboard provided"
            await ctx.followup.send(embed=embed)
            return

        r = 0
        for i in leaderboard:
            p = await self.bot.fetch_user(i[0])
            exp = i[4]
            r += 1
            embed.add_field(name=f"`{r}.` {p}", value=f"`{exp}XP`", inline=True)

        await ctx.followup.send(embed=embed)


class levelling(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.topggpy = DBLClient(bot=self.bot, token=TOPGG)
        self.profile_context = Jeanne.ContextMenu(
            name="Profile", callback=self.profile_generate
        )
        self.bot.tree.add_command(self.profile_context)
        self.profile_generate_error = self.profile_context.error(
            self.profile_generate_error
        )

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.profile_context.name, type=self.profile_context.type
        )

    async def generate_profile_card(self, ctx: Interaction, member: Member):
        try:
            #voted = await self.topggpy.get_user_vote(member.id)
            bg_image = Inventory(member).selected_wallpaper
            image = await Profile(self.bot).generate_profile(member, bg_image, False)
            file = File(fp=image, filename=f"{member.name}_profile_card.png")
            await ctx.followup.send(file=file)

        except:
            no_exp = Embed(description=f"Failed to make profile card")
            await ctx.followup.send(embed=no_exp)

    @Jeanne.checks.cooldown(1, 120, key=lambda i: (i.user.id))
    async def profile_generate(self, ctx: Interaction, member: Member):
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.profile.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return
        await ctx.response.defer()
        await self.generate_profile_card(ctx, member)

    async def profile_generate_error(self, ctx: Interaction, error: Exception) -> None:
        if isinstance(error, Jeanne.CommandOnCooldown):
            if Command(ctx.guild).check_disabled(self.profile.qualified_name):
                await ctx.response.send_message(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            cooldown = Embed(
                description=f"You have already used the profile command!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)

    @Cog.listener()
    async def on_message(self, message: Message):
        if Botban(message.author).check_botbanned_user or message.author.bot:
            return

        levelling_instance = Levelling(message.author, message.guild)
        if not levelling_instance.check_xpblacklist_channel(message.channel):
            try:
                level_data = await levelling_instance.add_xp()

                if level_data is None:
                    return

                channel, levelup, rankup = level_data
                role_reward = message.guild.get_role(levelling_instance.get_role_reward)

                parameters = OrderedDict(
                    [
                        ("%member%", str(message.author)),
                        ("%pfp%", str(message.author.display_avatar)),
                        ("%server%", str(message.guild.name)),
                        ("%mention%", str(message.author.mention)),
                        ("%name%", str(message.author.name)),
                        ("%newlevel%", str(levelling_instance.get_member_level)),
                        ("%role%", str(role_reward.name if role_reward else None)),
                        (
                            "%rolemention%",
                            str(role_reward.mention if role_reward else None),
                        ),
                    ]
                )

                content = ""
                embed = None

                if role_reward!=None:
                    await message.author.add_roles(role_reward)

                    try:
                        json_data: dict = loads(replace_all(rankup, parameters))
                        content: str = json_data.get("content")
                        embed = Embed.from_dict(json_data.get("embeds", [{}])[0])
                    except:
                        content = f"CONGRATS {message.author}! You were role awarded {role_reward.name}"

                elif levelup is not None:
                    try:
                        json_data = loads(replace_all(levelup, parameters))
                        content = json_data.get("content")
                        embed = Embed.from_dict(json_data.get("embeds", [{}])[0])
                    except:
                        content = f"CONGRATS {message.author}! You leveled up to level {levelling_instance.get_member_level}"

                elif levelup is not None:
                    try:
                        json_data = loads(replace_all(levelup, parameters))
                        content = json_data.get("content")
                        embed = Embed.from_dict(json_data.get("embeds", [{}])[0])
                    except:
                        content = f"{message.author} has leveled up to `level {levelling_instance.get_member_level}`"

                await self.send_level_message(channel, content, embed)

            except AttributeError:
                pass

    async def send_level_message(
        self, channel_id: Optional[int], content: str, embed: Optional[Embed]
    ):
        if channel_id is not None:
            lvlup_channel = await self.bot.fetch_channel(channel_id)
            await lvlup_channel.send(content=content, embed=embed)

    @Jeanne.command(description="See your profile or someone else's profile")
    @Jeanne.describe(member="Which member?")
    @Jeanne.checks.cooldown(1, 120, key=lambda i: (i.user.id))
    async def profile(self, ctx: Interaction, member: Optional[Member] = None) -> None:
        if Botban(ctx.user).check_botbanned_user:
            return
        if Command(ctx.guild).check_disabled(self.profile.qualified_name):
            await ctx.response.send_message(
                "This command is disabled by the server's managers", ephemeral=True
            )
            return

        member = ctx.user if member == None else member
        await ctx.response.defer()
        await self.generate_profile_card(ctx, member)

    @profile.error
    async def profile_error(self, ctx: Interaction, error: Jeanne.AppCommandError):
        if isinstance(error, Jeanne.CommandOnCooldown):
            if Command(ctx.guild).check_disabled(self.profile.qualified_name) == True:
                await ctx.response.send_message(
                    "This command is disabled by the server's managers", ephemeral=True
                )
                return
            cooldown = Embed(
                description=f"You have already used the profile command!\nTry again after `{round(error.retry_after, 2)} seconds`",
                color=Color.red(),
            )
            await ctx.response.send_message(embed=cooldown)


async def setup(bot: Bot):
    await bot.add_cog(Rank_Group(bot))
    await bot.add_cog(levelling(bot))
