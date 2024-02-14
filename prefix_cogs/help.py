from json import dumps, loads
from typing import Mapping
from discord import ButtonStyle, Color, Embed, ui
from discord.ext.commands import Bot, Cog, group, Context, Range
from discord.ext import commands as Jeanne
from functions import Botban
from collections import OrderedDict
from assets.help.modules import modules, Modules
from reactionmenu import ViewMenu, ViewButton


def replace_all(text: str, dic: dict):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


class help_button(ui.View):
    def __init__(self):
        super().__init__()

        wiki_url = "https://jeannebot.gitbook.io/jeannebot/help"
        orleans_url = "https://discord.gg/jh7jkuk2pp"
        tos_and_policy_url = "https://jeannebot.gitbook.io/jeannebot/tos-and-privacy"

        self.add_item(
            ui.Button(style=ButtonStyle.link, label="Jeanne Webiste", url=wiki_url)
        )
        self.add_item(
            ui.Button(style=ButtonStyle.link, label="Support Server", url=orleans_url)
        )
        self.add_item(
            ui.Button(
                style=ButtonStyle.link,
                label="ToS and Privacy Policy",
                url=tos_and_policy_url,
            )
        )


class HelpGroupPrefix(Cog, name="Help"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @group(
        invoke_without_command=True,
        description="Main Help command for the help subcommands",
    )
    async def help(self, ctx: Context): 
        ...

    @help.command(
        aliases=["allcmds"],
        description="Get a list of all the available commands"
    )
    async def allcommands(self, ctx: Context):
        await ctx.typing()
        embed = Embed(
            color=Color.random(),
            description="Here is a list of all commands in their modules"
        )
        excluded_cogs = ["Jishaku", "Owner"]
        for cog_name, cog in self.bot.cogs.items():
            if cog_name not in excluded_cogs:
                cmds = [command.qualified_name for command in cog.walk_commands()]
                if cmds:
                    embed.add_field(
                        name=cog_name,
                        value="\n".join(cmds),
                        inline=True
                    )
        await ctx.send(embed=embed)


    @help.command(aliases=["cmd"], description="Get help on a certain command")
    async def command(self, ctx: Context, *, command: Range[str, 3]):
        if Botban(ctx.author).check_botbanned_user:
            return

        await ctx.defer()
        cmd = next(
            (
                cmd
                for cmd in self.bot.walk_commands()
                if not isinstance(cmd, Jeanne.Group) and cmd.qualified_name == command
            ),
            None,
        )

        if cmd:
            bot_perms: dict = getattr(cmd, "bot_perms", None)
            member_perms: dict = getattr(cmd, "member_perms", None)

            embed = Embed(title=f"{command.title()} Help", color=Color.random())
            embed.description = cmd.description

            if len(cmd.aliases) >= 1:
                embed.add_field(
                    name="Aliases", value=", ".join(cmd.aliases), inline=True
                )
            parms = cmd.signature

            if parms:
                embed.add_field(name="Parameters", value=parms, inline=False)

            if bot_perms:
                perms = [str(i).replace("_", " ").title() for i in bot_perms.keys()]
                embed.add_field(
                    name="Bot Permissions", value="\n".join(perms), inline=True
                )

            if member_perms:
                perms = [str(i).replace("_", " ").title() for i in member_perms.keys()]
                embed.add_field(
                    name="User Permissions", value="\n".join(perms), inline=True
                )

            cmd_usage = "j!" + cmd.qualified_name + " " + parms
            embed.add_field(name="Command Usage", value=f"`{cmd_usage}`", inline=False)
            embed.set_footer(
                text="Legend:\n<> - Required\n[] - Optional\n\nIt is best to go to the websites for detailed explanations and usages"
            )

            await ctx.send(embed=embed)
            return
        embed = Embed(description="I don't have this command", color=Color.red())
        await ctx.send(embed=embed)

    @help.command(description="Get help of a certain module")
    async def module(self, ctx: Context, module: str):
        if Botban(ctx.author).check_botbanned_user:
            return
        await ctx.defer()

        module_mapping = {
            "currency": Modules.currency,
            "fun": Modules.fun,
            "hentai": Modules.hentai,
            "image": Modules.image,
            "pictures": Modules.image,
            "pics": Modules.image,
            "images": Modules.image,
            "info": Modules.info,
            "information": Modules.info,
            "levelling": Modules.levelling,
            "lvl": Modules.levelling,
            "rank": Modules.levelling,
            "moderation": Modules.moderation,
            "mod": Modules.moderation,
            "reactions": Modules.reactions,
            "react": Modules.reactions,
        }

        module_instance = module_mapping.get(module.lower())

        module_data = dumps(modules[module_instance.value])

        if module_data:
            parms = OrderedDict([("%module%", str(module.capitalize()))])

            json_data: dict = loads(replace_all(module_data, parms))

            embed_data = json_data.get("embeds")
            embed = Embed.from_dict(embed_data[0])

        await ctx.send(embed=embed)

    @help.command(
        description="Get help from the website or join the support server for further help"
    )
    async def support(self, ctx: Context):
        if Botban(ctx.author).check_botbanned_user:
            return

        view = help_button()
        help = Embed(
            description="Click on one of the buttons to open the documentation or get help in the support server",
            color=Color.random(),
        )
        await ctx.send(embed=help, view=view)


async def setup(bot: Bot):
    await bot.add_cog(HelpGroupPrefix(bot))
