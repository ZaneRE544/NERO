from nextcord import *
from nextcord.ui import *

misc = Embed(title="Misc Module", color=0x7DF9FF)
misc.add_field(name='Available commands',
                 value="• Invite\n• Say\n• Report")
misc.set_footer(
    text="If you need extended help about the use of commands, use the drop menu below")

class mischelp(ui.Select):
    def __init__(self):

        options=[
            SelectOption(label="Invite"), SelectOption(
                label="Say"), SelectOption(label="Report")
        ]

        super().__init__(placeholder='What command you need help on?', options=options)

    async def callback(self, ctx: Interaction):
        if self.values[0]=="Invite":
            await ctx.response.defer(ephemeral=True)
            userinfo = Embed(color=0x7DF9FF)
            userinfo.add_field(
                name="Invite me to your server or join my creator's server", value="• **Example:** `/userinfo (IF YOURSELF)` \ `/userinfo MEMBER` (IF MEMBER)\n• **Expected result**: `MEMBER'S DISCORD INFORMATION INCLUDING THEIR SERVER JOIN DATE`")
            await ctx.edit_original_message(embed=userinfo, ephemeral=True)
        if self.values[0] == "Serverinfo":
            await ctx.response.defer(ephemeral=True)
            Serverinfo = Embed(color=0x7DF9FF)
            Serverinfo.add_field(
                name="Get information about this server", value="• **Example:** `/serverinfo`\n• **Expected result**: `INFORMATION ABOUT THE SERVER AND EMOJIS IN A SEPERATE EMBED IF APPLICABLE`")
            await ctx.edit_original_message(embed=Serverinfo, ephemeral=True)
        if self.values[0] == "Ping":
            await ctx.response.defer(ephemeral=True)
            ping = Embed(color=0x7DF9FF)
            ping.add_field(
                name="Check how fast I can respond to commands", value="• **Example:** `/ping`\n• **Expected result**: `JEANNE FIRST CHECKS LATENCY THEN EDITS THE MESSAGE WITH 2 PING RESULTS (ONE WITH BOT AND OTHER WITH API)`")
            await ctx.edit_original_message(embed=ping, ephemeral=True)
        if self.values[0] == "Stats":
            await ctx.response.defer(ephemeral=True)
            saber = Embed(color=0x7DF9FF)
            saber.add_field(
                name="See the bot's status from development to now", value="• **Example:** `/stats`\n• **Expected result**: `JEANNE SHOWS AS MUCH INFO OF HERSELF`")
            await ctx.edit_original_message(embed=saber, ephemeral=True)
        if self.values[0] == "Guild Banner":
            await ctx.response.defer(ephemeral=True)
            saber = Embed(color=0x7DF9FF)
            saber.add_field(
                name="See the server's banner\n• **NOTE:** If the server is not boosted to Level 2, it will return with a `Not boosted to Level 2` error. If the server doesn't have a banner, it will return with a footer text only.", value="• **Example:** `/guildbanner`\n• **Expected result**: `SERVER'S BANNER IF APPLICABLE`\n• **Expected failure**: `SERVER NOT BOOSTED TO LEVEL 2 ERROR OR NO SERVER BANNER FOUND`")
            await ctx.edit_original_message(embed=saber, ephemeral=True)
        if self.values[0] == "Avatar":
            await ctx.response.defer(ephemeral=True)
            saber = Embed(color=0x7DF9FF)
            saber.add_field(
                name="See your avatar or a member's avatar", value="• **Example:** `/avatar` (IF YOURSELF) / `/avatar MEMBER` (IF MEMBER)\n• **Expected result**: `MEMBERS'S AVATAR`")
            await ctx.edit_original_message(embed=saber, ephemeral=True)
        if self.values[0] == "Guild Avatar":
            await ctx.response.defer(ephemeral=True)
            saber = Embed(color=0x7DF9FF)
            saber.add_field(
                name="See your guild avatar or a member's guild avatar\n• **NOTE:** If the member has no guild avatar set, it will return with their normal avatar.", value="• **Example:** `/guildavatar` (IF YOURSELF) / `/guildavatar MEMBER` (IF MEMBER)\n• **Expected result**: `MEMBERS'S SERVER AVATAR`\n• **Expected failure**: `MEMBERS'S NORMAL AVATAR WITH FOOTER TEXT`")
            await ctx.edit_original_message(embed=saber, ephemeral=True)


class miscview(View):
    def __init__(self):
        super().__init__()
        self.add_item(mischelp())

        
