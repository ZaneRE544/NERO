from discord import (
    ui,
    ButtonStyle,
    Interaction,
    User,
    SelectOption,
    AllowedMentions,
    Color,
    Embed,
    SyncWebhook,
    TextChannel,
    TextStyle,
)
from typing import Optional
from collections import OrderedDict
from json import loads
from config import WEBHOOK
from functions import Levelling, Welcomer


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


class Confirmation(ui.View):
    def __init__(self, author: User):
        super().__init__(timeout=60)
        self.author = author
        self.value = None

    @ui.button(label="Confirm", style=ButtonStyle.green)
    async def confirm(self, ctx: Interaction, button: ui.Button):
        self.value = True
        button.disabled = True
        self.stop()

    @ui.button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, ctx: Interaction, button: ui.Button):
        self.value = False
        button.disabled = True
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class Heads_or_Tails(ui.View):
    def __init__(self, author: User):
        self.author = author
        super().__init__(timeout=30)
        self.value = None

    @ui.button(label="Heads", style=ButtonStyle.green)
    async def confirm(self, button: ui.Button, ctx: Interaction):
        self.value = "Heads"
        self.stop()

    @ui.button(label="Tails", style=ButtonStyle.green)
    async def cancel(self, button: ui.Button, ctx: Interaction):
        self.value = "Tails"
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class Cancellation(ui.View):
    def __init__(self, author: User):
        super().__init__()
        self.author = author
        self.value = None

    @ui.button(label="Cancel", style=ButtonStyle.red)
    async def cancel(self, ctx: Interaction, button: ui.Button):
        self.value = "cancel"
        button.disabled = True
        self.stop()

    async def interaction_check(self, ctx: Interaction):
        return ctx.user.id == self.author.id


class Welcomingmsg(ui.Modal, title="Welcoming Message"):
    def __init__(self) -> None:
        super().__init__()

    jsonscript = ui.TextInput(
        label="JSON",
        style=TextStyle.paragraph,
        placeholder="Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
        required=True,
        min_length=1,
        max_length=4000,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        humans = str(len([member for member in ctx.guild.members if not member.bot]))
        parameters = OrderedDict(
            [
                ("%member%", str(ctx.user)),
                ("%pfp%", str(ctx.user.display_avatar)),
                ("%server%", str(ctx.guild.name)),
                ("%mention%", str(ctx.user.mention)),
                ("%name%", str(ctx.user.name)),
                ("%members%", str(ctx.guild.member_count)),
                ("%humans%", str(humans)),
                ("%icon%", str(ctx.guild.icon)),
            ]
        )

        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json["embeds"][0])
        except:
            content = replace_all(self.jsonscript.value, parameters)

        confirm = Embed(
            description="This is the preview of the welcoming message.\nAre you happy with it?"
        )

        view = Confirmation(ctx.user)
        try:
            embeds = [embed, confirm]
        except:
            embeds = [confirm]
        await ctx.response.send_message(
            content=content,
            embeds=embeds,
            view=view,
            allowed_mentions=AllowedMentions(everyone=False, roles=False, users=False),
            ephemeral=True,
        )
        await view.wait()

        if view.value == True:
            Welcomer(ctx.guild).set_welcomer_msg(self.jsonscript.value)

            embed = Embed(description="Welcoming message set")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)

        elif view.value == False:
            embed = Embed(description="Action cancelled")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)
        else:
            embed = Embed(description="Timeout")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)


class Leavingmsg(ui.Modal, title="Leaving Message"):
    def __init__(self) -> None:
        super().__init__()

    jsonscript = ui.TextInput(
        label="JSON",
        style=TextStyle.paragraph,
        placeholder="Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
        required=True,
        min_length=1,
        max_length=4000,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        humans = str(len([member for member in ctx.guild.members if not member.bot]))
        parameters = OrderedDict(
            [
                ("%member%", str(ctx.user)),
                ("%pfp%", str(ctx.user.display_avatar)),
                ("%server%", str(ctx.guild.name)),
                ("%mention%", str(ctx.user.mention)),
                ("%name%", str(ctx.user.name)),
                ("%members%", str(ctx.guild.member_count)),
                ("%humans%", str(humans)),
                ("%icon%", str(ctx.guild.icon)),
            ]
        )

        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json["embeds"][0])
        except:
            content = replace_all(self.jsonscript.value, parameters)

        confirm = Embed(
            description="This is the preview of the leaving message.\nAre you happy with it?"
        )

        view = Confirmation(ctx.user)
        try:
            embeds = [embed, confirm]
        except:
            embeds = [confirm]
        await ctx.response.send_message(
            content=content,
            embeds=embeds,
            view=view,
            allowed_mentions=AllowedMentions(everyone=False, roles=False, users=False),
            ephemeral=True,
        )
        await view.wait()

        if view.value == True:
            Welcomer(ctx.guild).set_leaving_msg(self.jsonscript.value)

            embed = Embed(description="Leaving message set")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)

        elif view.value == False:
            embed = Embed(description="Action cancelled")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)
        else:
            embed = Embed(description="Timeout")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)


class Levelmsg(ui.Modal, title="Level Update Message"):
    def __init__(self, channel: TextChannel) -> None:
        super().__init__()
        self.channel = channel

    jsonscript = ui.TextInput(
        label="JSON",
        style=TextStyle.paragraph,
        placeholder="Insert JSON script here. If you don't have, type a plain message as long it follows the parameters",
        required=True,
        min_length=1,
        max_length=4000,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        Levelling(server=ctx.guild).add_level_channel(self.channel)
        parameters = OrderedDict(
            [
                ("%member%", str(ctx.user)),
                ("%pfp%", str(ctx.user.display_avatar)),
                ("%server%", str(ctx.guild.name)),
                ("%mention%", str(ctx.user.mention)),
                ("%name%", str(ctx.user.name)),
                ("%newlevel%", str(Levelling(ctx.user, ctx.guild).get_member_level())),
            ]
        )

        try:
            json = loads(replace_all(self.jsonscript.value, parameters))
            content = json["content"]
            embed = Embed.from_dict(json["embeds"][0])
        except:
            content = replace_all(self.jsonscript.value, parameters)

        confirm = Embed(
            description="This is the preview of the level update message whenever someone levels up in the server and will be sent to {}.\nAre you happy with it?".format(
                self.channel.mention
            )
        )

        view = Confirmation(ctx.user)
        try:
            embeds = [embed, confirm]
        except:
            embeds = [confirm]
        await ctx.response.send_message(
            content=content,
            embeds=embeds,
            view=view,
            allowed_mentions=AllowedMentions(everyone=False, roles=False, users=False),
            ephemeral=True,
        )
        await view.wait()

        if view.value == True:
            Levelling(server=ctx.guild).add_level_channel(
                self.channel, self.jsonscript.value
            )

            embed = Embed(description="Level update message set")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)

        elif view.value == False:
            embed = Embed(description="Action cancelled")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)
        else:
            embed = Embed(description="Timeout")
            await ctx.edit_original_response(content=None, embeds=[embed], view=None)


class ReportModal(ui.Modal, title="Bot Report"):
    def __init__(self):
        super().__init__()

    report_type = ui.TextInput(
        label="Type of report",
        placeholder="Example: bug, fault, violator",
        required=True,
        min_length=10,
        max_length=30,
        style=TextStyle.short,
    )
    report = ui.TextInput(
        label="Problem",
        placeholder="Type the problem here",
        required=True,
        min_length=10,
        max_length=2000,
        style=TextStyle.paragraph,
    )

    steps = ui.TextInput(
        label="Steps of how you got this problem",
        placeholder="Type the steps here",
        required=False,
        min_length=10,
        max_length=1024,
        style=TextStyle.paragraph,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        report = Embed(title=self.report_type.value, color=Color.brand_red())
        report.description = self.report.value
        if self.steps.value != None or "":
            report.add_field(name="Steps", value=self.steps.value, inline=False)
        report.set_footer(text="Reporter {}| `{}`".format(ctx.user, ctx.user.id))
        SyncWebhook.from_url(WEBHOOK).send(embed=report)
        embed = Embed(
            description="Thank you for submitting your bot report. The dev will look into it but the will not tell you the results.\n\nPlease know that your user ID has been logged if you are trolling around."
        )
        await ctx.response.send_message(embed=embed)


class ReportContentM(ui.Modal, title="Illicit Content Report"):
    def __init__(self, link: str):
        self.link = link
        super().__init__()

    illegalcontent = ui.TextInput(
        label="Reason",
        style=TextStyle.short,
        placeholder="Why are you reporting this link? (eg. loli hentai, too much blood)",
        required=True,
        min_length=4,
        max_length=256,
    )

    async def on_submit(self, ctx: Interaction) -> None:
        report = Embed(title="Illicit Content Reported", color=Color.brand_red())
        report.add_field(name="Link", value=self.link, inline=False)
        report.add_field(name="Reason", value=self.illegalcontent.value, inline=False)
        report.set_footer(text="Reporter {}| `{}`".format(ctx.user, ctx.user.id))
        SyncWebhook.from_url(WEBHOOK).send(embed=report)
        embed = Embed(
            description="Than you for submitting the report.\n\nPlease know that your user ID has been logged if you are trolling around."
        )
        await ctx.response.send_message(embed=embed, ephemeral=True)


class ReportContentPlus(ui.Select):
    def __init__(
        self,
        link1: Optional[str] = None,
        link2: Optional[str] = None,
        link3: Optional[str] = None,
        link4: Optional[str] = None,
    ):
        self.link1 = link1
        self.link2 = link2
        self.link3 = link3
        self.link4 = link4
        options = [
            SelectOption(label="Report 1st Media", value=self.link1),
            SelectOption(label="Report 2nd Media", value=self.link2),
            SelectOption(label="Report 3rd Media", value=self.link3),
            SelectOption(label="Report 4th Media", value=self.link4),
        ]
        super().__init__(
            placeholder="Saw something illegal? Report it here",
            max_values=1,
            min_values=1,
            options=options,
        )

    async def callback(self, ctx: Interaction):
        await ctx.response.send_modal(ReportContentM(self.values[0]))


class ReportSelect(ui.View):
    def __init__(
        self,
        link1: Optional[str] = None,
        link2: Optional[str] = None,
        link3: Optional[str] = None,
        link4: Optional[str] = None,
    ):
        self.link1 = link1
        self.link2 = link2
        self.link3 = link3
        self.link4 = link4
        super().__init__()
        self.add_item(ReportContentPlus(self.link1, self.link2, self.link3, self.link4))


class ReportContent(ui.View):
    def __init__(self, link: str):
        super().__init__()
        self.link = link

    @ui.button(label="Report Content", style=ButtonStyle.grey)
    async def report1(self, ctx: Interaction, button: ui.Button):
        self.value = "report"
        await ctx.response.send_modal(ReportContentM(self.link))