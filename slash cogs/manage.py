from db_functions import *
from nextcord import *
from nextcord import slash_command as jeanne_slash
from nextcord.ext.commands import Cog, Bot
from nextcord.abc import GuildChannel
from nextcord.ext.application_checks import *
from humanfriendly import format_timespan, parse_timespan


class slashmanage(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @jeanne_slash(description="Add a role to a member")
    @has_permissions(manage_roles=True)
    async def add_role(self, ctx: Interaction, member: Member = SlashOption(description="Which member?"), role: Role = SlashOption(description="Which role will you add?")):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await member.add_roles(role)
            embed = Embed(color=0x00FF68)
            embed.add_field(name=f"Role given",
                            value=f"`{role}` was given to `{member}`", inline=False)
            await ctx.followup.send(embed=embed)

    @jeanne_slash(description="Remove a role from a member")
    @has_permissions(manage_roles=True)
    async def remove_role(self, ctx: Interaction, member: Member = SlashOption(description="Which member?"), role: Role = SlashOption(description="Which role will you delete?")):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await member.remove_roles(role)
            embed = Embed(color=0x00FF68)
            embed.add_field(name=f"Role removed",
                            value=f"`{role}` was removed from `{member}`", inline=False)
            await ctx.followup.send(embed=embed)

    @jeanne_slash(description="Main create command")
    async def create(self, ctx: Interaction):
        pass

    @create.subcommand(description='Create a text channel')
    @has_permissions(manage_channels=True)
    async def text_channel(self, ctx: Interaction, name: str = SlashOption(description="What will you name it?", required=True), category: GuildChannel = SlashOption(description="Which category will it be placed?", channel_types=[ChannelType.category], required=False), slowmode: str = SlashOption(description="How long is the slowmode (1s, 1h30m)? Maxinum is 6 hours", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:

            embed = Embed()
            embed.color = Color.green()
            embed.description = "Text Channel `{}` has been created".format(
                name)

            if category:
                channel = await ctx.guild.create_text_channel(name=name, category=category)
                embed.add_field(name="Added into category",
                                value=category.name, inline=True)

            else:
                channel = await ctx.guild.create_text_channel(name)

            if slowmode:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await channel.edit(slowmode_delay=delay)
                embed.add_field(name="Slowmode",
                                value=format_timespan(delay), inline=True)

            await ctx.followup.send(embed=embed)

    @create.subcommand(description='Create a text channel')
    @has_permissions(manage_channels=True)
    async def voice_channel(self, ctx: Interaction, name: str = SlashOption(description="What will you name it?", required=True), category: GuildChannel = SlashOption(description="Which category will it be placed?", channel_types=[ChannelType.category], required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:

            embed = Embed()
            embed.description = "Voice Channel `{}` has been created".format(
                name)
            embed.color = Color.green()

            if category:
                await ctx.guild.create_voice_channel(name=name, category=category)
                embed.add_field(name="Added into category",
                                value=category.name, inline=True)

            else:
                await ctx.guild.create_voice_channel(name)

            await ctx.followup.send(embed=embed)

    @create.subcommand(description='Create a category')
    @has_permissions(manage_channels=True)
    async def category(self, ctx: Interaction, name: str = SlashOption(description="What will you name it?", required=True)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.guild.create_category(name=name)
            embed = Embed()
            embed.description = "Category `{}` has been created".format(name)
            embed.color = Color.green()

            await ctx.followup.send(embed=embed)

    @create.subcommand(description='Create a stage channel')
    @has_permissions(manage_channels=True)
    async def stage_channel(self, ctx: Interaction, name: str = SlashOption(description="What will you name it?", required=True), topic: str = SlashOption(required=True), category: GuildChannel = SlashOption(description="Which category will it be placed?", channel_types=[ChannelType.category], required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.guild.create_stage_channel(name=name, topic=topic, category=category)
            embed = Embed()
            embed.description = "Stage channel `{}` has been created".format(
                name)
            embed.color = Color.green()

            await ctx.followup.send(embed=embed)

    @create.subcommand(description="Create a forum [experimental]. If you see an error message but it exists, it works but improperly")
    @has_permissions(manage_channels=True)
    async def forum(self, ctx: Interaction, name: str = SlashOption(description="What will you name it?", required=True), topic: str = SlashOption(description="What is the topic?", required=True), category: GuildChannel = SlashOption(description="Which category will it be placed?", channel_types=[ChannelType.category], required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            forum = await ctx.guild.create_forum_channel(name=name, topic=topic)
            embed = Embed()
            embed.description = "Forum `{}` has been created".format(
                forum.name)
            embed.color = Color.green()
            if category:
                await forum.edit(category=category)
                embed.add_field(name="Added into category",
                                value=category.name, inline=True)

            await ctx.followup.send(embed=embed)

    @create.subcommand(description="Create a role")
    @has_permissions(manage_roles=True)
    async def role(self, ctx: Interaction, name=SlashOption(description="What will you name it?", required=True), color=SlashOption(required=False), hoisted=SlashOption(choices=["True", "False"], description="Should it be displayed seperately in the members list?", required=False), mentionable=SlashOption(choices=["True", "False"], description="Should it be mentionable?", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            role = await ctx.guild.create_role(name=name)
            embed = Embed()
            embed.description = "Role `{}` has been created".format(name)
            embed.color = Color.green()

            if color:
                await role.edit(color=int(color, 16))
                embed.add_field(name="Color", value=color, inline=True)

            if hoisted:
                if hoisted == "True":
                    await role.edit(hoist=True)
                    embed.add_field(name="Hoisted", value="Yes", inline=True)
                elif hoisted == "False":
                    pass

            if mentionable:
                if mentionable == "True":
                    await role.edit(mentionable=True)
                    embed.add_field(name="Mentionable",
                                    value="Yes", inline=True)
                elif mentionable == "False":
                    pass

            await ctx.followup.send(embed=embed)

    @create.subcommand(description="Makes a thread channel")
    @has_permissions(create_public_threads=True)
    async def thread(self, ctx: Interaction, name: str = SlashOption(required=True), message_id=SlashOption(description="Add the message ID here", required=True), slowmode: str = SlashOption(description="How long is the slowmode (1s, 1h30m)? Maxinum is 6 hours", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            message = await ctx.channel.fetch_message(message_id)
            thread = await ctx.channel.create_thread(name=name, message=message, type=ChannelType.public_thread)

            embed = Embed()
            embed.description = "Thread `{}` has been created on [message]({})".format(
                name, message.jump_url)
            embed.color = Color.green()

            if slowmode:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await thread.edit(slowmode_delay=delay)
                embed.add_field(name="Slowmode",
                                value=format_timespan(delay), inline=True)

            await ctx.followup.send(embed=embed)

    @jeanne_slash(description="Main delete command")
    async def delete(self, ctx: Interaction):
        pass

    @delete.subcommand(description="Deletes a channel")
    @has_permissions(manage_channels=True)
    async def channel(self, ctx: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.text,   ChannelType.voice, ChannelType.category, ChannelType.news, ChannelType.public_thread, ChannelType.private_thread], description="Choose a channel to delete", required=True)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await channel.delete()
            embed = Embed(description="{} has been deleted".format(
                channel.name), color=0x00FF68)
            await ctx.followup.send(embed=embed)

    @delete.subcommand(name="role", description="Deletes a role")
    @has_permissions(manage_channels=True)
    async def role_1(self, ctx: Interaction, role: Role = SlashOption(description="Choose a role to delete", required=True)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await role.delete()
            embed = Embed(description="{} has been deleted".format(
                role.name), color=0x00FF68)
            await ctx.followup.send(embed=embed)

    @jeanne_slash(description="Main edit command")
    async def edit(self, ctx: Interaction):
        pass

    @edit.subcommand(name="text_channel", description="Edits a text/news channel")
    @has_permissions(manage_channels=True)
    async def text_channel_1(self, ctx: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.news, ChannelType.text], required=True), name: str = SlashOption(required=False), nsfw_enabled=SlashOption(choices=["True", "False"], required=False), slowmode: str = SlashOption(description="How long is the slowmode (1s, 1h30m)? Maxinum is 6 hours", required=False), category: GuildChannel = SlashOption(channel_types=[ChannelType.category], required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            embed = Embed()
            embed.description = "Channel `{}` has been edited".format(
                channel.name)
            embed.color = Color.green()

            if name:
                await channel.edit(name=name)
                embed.add_field(name="Name", value=name, inline=True)

            if category:
                await channel.edit(category=category)
                embed.add_field(name="Category",
                                value=category, inline=True)

            if nsfw_enabled:
                if nsfw_enabled == "True":
                    await channel.edit(nsfw=True)
                    embed.add_field(name="NSFW enabled",
                                    value="Yes", inline=True)
                elif nsfw_enabled == "False":
                    await channel.edit(nsfw=False)
                    embed.add_field(name="NSFW enabled",
                                    value="No", inline=True)

            if slowmode:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await channel.edit(slowmode_delay=delay)
                embed.add_field(name="Slowmode",
                                value=format_timespan(delay), inline=True)

            await ctx.followup.send(embed=embed)

    @edit.subcommand(name="thread", description="Edits a thread")
    @has_permissions(manage_channels=True)
    async def thread_1(self, ctx: Interaction, thread: GuildChannel = SlashOption(channel_types=[ChannelType.private_thread, ChannelType.public_thread], required=True), name: str = SlashOption(required=False), slowmode: str = SlashOption(description="How long is the slowmode (1s, 1h30m)? Maxinum is 6 hours", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            embed = Embed()
            embed.description = "Thread `{}` has been edited".format(
                thread.name)
            embed.color = Color.green()

            if name:
                await thread.edit(name=name)
                embed.add_field(name="Name", value=name, inline=True)

            if slowmode:
                delay = int(parse_timespan(slowmode))
                if delay > 21600:
                    delay = 21600
                await thread.edit(slowmode_delay=delay)
                embed.add_field(name="Slowmode",
                                value=format_timespan(delay), inline=True)

            await ctx.followup.send(embed=embed)

    @edit.subcommand(name="role", description="Edit a role")
    @has_permissions(manage_roles=True)
    async def role_2(self, ctx: Interaction, role: Role = SlashOption(required=True), name: str = SlashOption(description="What will you name it?", required=False), color=SlashOption(required=False), hoisted=SlashOption(choices=["True", "False"], description="Should it be displayed seperately in the members list?", required=False), mentionable=SlashOption(choices=["True", "False"], description="Should it be mentionable?", required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            embed = Embed()
            embed.description = "Role `{}` has been edited".format(role.name)
            embed.color = Color.green()

            if name:
                await role.edit(name=name)
                embed.add_field(name="Name", value=name, inline=True)

            if color:
                await role.edit(color=int(color, 16))
                embed.add_field(name="Color", value=color, inline=True)

            if hoisted:
                if hoisted == "True":
                    await role.edit(hoist=True)
                    embed.add_field(name="Hoisted", value="Yes", inline=True)
                elif hoisted == "False":
                    await role.edit(hoist=False)
                    embed.add_field(name="Hoisted", value="No", inline=True)

            if mentionable:
                if mentionable == "True":
                    await role.edit(mentionable=True)
                    embed.add_field(name="Mentionable",
                                    value="Yes", inline=True)
                elif mentionable == "False":
                    await role.edit(mentionable=False)
                    embed.add_field(name="Mentionable",
                                    value="No", inline=True)

            await ctx.followup.send(embed=embed)

    @edit.subcommand(description="Edits the server")
    @has_permissions(manage_guild=True)
    async def server(self, ctx: Interaction, name: str = SlashOption(required=False), description: str = SlashOption(required=False), verification_level=SlashOption(choices=['none', 'low', 'medium', 'high', 'highest'], required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            embed = Embed()
            embed.description = "{} has been edited".format(ctx.guild.name)
            embed.color = Color.green()

            if name:
                await ctx.guild.edit(name=name)
                embed.add_field(name="Name", value=name, inline=True)

            if description:
                if "PUBLIC" in ctx.guild.features:
                    await ctx.guild.edit(description=description)
                    embed.add_field(name="Description",
                                    value=description, inline=True)
                else:
                    embed.add_field(name="Description",
                                    value="Your server is not public to have a description edited", inline=True)


            if verification_level:
                if verification_level == 'none':
                    await ctx.guild.edit(verification_level=VerificationLevel.none)
                    embed.add_field(name="Verification Level", value="{}\nNo verification required".format(
                        verification_level), inline=True)

                elif verification_level == 'low':
                    await ctx.guild.edit(verification_level=VerificationLevel.low)
                    embed.add_field(name="Verification Level", value="{}\nMembers must have a verified email".format(
                        verification_level), inline=True)

                elif verification_level == 'medium':
                    await ctx.guild.edit(verification_level=VerificationLevel.medium)
                    embed.add_field(name="Verification Level", value="{}\nMembers must have a verified email and be registered on Discord for more than 5 minutes".format(
                        verification_level), inline=True)

                elif verification_level == 'high':
                    await ctx.guild.edit(verification_level=VerificationLevel.high)
                    embed.add_field(name="Verification Level", value="{}\nMembers must have a verified email, be registered on Discord for more than 5 minutes and stay in the server for more than 10 minutes".format(
                        verification_level), inline=True)

                elif verification_level == 'highest':
                    await ctx.guild.edit(verification_level=VerificationLevel.highest)
                    embed.add_field(name="Verification Level", value="{}\nMembers must have a verified phone number".format(
                        verification_level), inline=True)

            await ctx.followup.send(embed=embed)

    @edit.subcommand(name="forum", description="Edits a forum")
    @has_permissions(manage_channels=True)
    async def forum_1(self, ctx: Interaction, forum: GuildChannel = SlashOption(channel_types=[ChannelType.forum]), name: str = SlashOption(description="What will you name it?", required=False), topic: str = SlashOption(description="What is the topic?", required=False), category: GuildChannel = SlashOption(description="Which category will it be placed?", channel_types=[ChannelType.category], required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:

            embed = Embed()
            embed.description = "Forum {} has been edited".format(forum.name)
            embed.color = Color.green()

            if name:
                await forum.edit(name=name)
                embed.add_field(name="Name",
                                value=name, inline=True)

            if topic:
                await forum.edit(topic=topic)
                embed.add_field(name="Topic",
                                value=topic, inline=True)

            if category:
                await forum.edit(category=category)
                embed.add_field(name="Category",
                                value=category, inline=True)

            await ctx.followup.send(embed=embed)

    @jeanne_slash(description="Removes a welcoming/modlog/report channel that was set from the database")
    @has_permissions(manage_guild=True)
    async def remove(self, ctx: Interaction, type=SlashOption(choices=['welcomer', 'leaver', 'modlog', 'report', 'all'], description='Which one or all?')):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if type == 'welcomer':
                wel = remove_welcomer(ctx.guild.id)

                if wel == False:
                    await ctx.followup.send("You don't have a welcomer channel")
                else:
                    welcomer = Embed(
                        description="Welcomer channel removed", color=0x00FF68)
                    await ctx.followup.send(embed=welcomer)

            elif type == 'leaver':
                leave = remove_leaver(ctx.guild.id)

                if leave == False:
                    await ctx.followup.send("You don't have a leaver channel")
                else:
                    leaver = Embed(
                        description="Leaver channel removed", color=0x00FF68)
                    await ctx.followup.send(embed=leaver)

            elif type == 'modlog':
                modloger = remove_modloger(ctx.guild.id)

                if modloger == False:
                    await ctx.followup.send("You don't have a modlog channel")
                else:
                    modlog = Embed(
                        description="Modlog channel removed", color=0x00FF68)
                    await ctx.followup.send(embed=modlog)

            elif type == 'report':
                reporter = remove_reporter(ctx.guild.id)

                if reporter == False:
                    await ctx.followup.send("You don't have a report channel")
                else:
                    report = Embed(
                        description="Report channel removed", color=0x00FF68)
                    await ctx.followup.send(embed=report)

            elif type == 'all':

                try:
                    remove_welcomer(ctx.guild.id) is True
                except:
                    pass

                try:
                    remove_leaver(ctx.guild.id) is True
                except:
                    pass

                try:
                    remove_modloger(ctx.guild.id) is True
                except:
                    pass

                try:
                    remove_reporter(ctx.guild.id) is True
                except:
                    pass

                all = Embed(
                    description='All channels that were set for the server have been removed from the database.', color=0x00FF68)
                await ctx.followup.send(embed=all)

    @jeanne_slash(description="Main set command")
    async def set(self, ctx: Interaction):
        pass

    @set.subcommand(description="Set a welcomer/modlog/report channel")
    @has_permissions(manage_guild=True)
    async def log_channel(self, ctx: Interaction, type=SlashOption(choices=['welcomer', 'leaver', 'modlog', 'report_channel'], description="Which one are you setting?", required=True),
                  channel: GuildChannel = SlashOption(
            channel_types=[
                ChannelType.text, ChannelType.news],
            description="Choose a channel")):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if type == 'welcomer':
                set_welcomer(ctx.guild.id, channel.id)

                welcomer = Embed(color=0x00FF68)
                welcomer.add_field(
                    name="Welcomer channel set", value=f"{channel.mention} has been selected to welcomer members in the server.")
                await ctx.followup.send(embed=welcomer)

            elif type == 'leaver':
                set_leaver(ctx.guild.id, channel.id)

                leaver = Embed(color=0x00FF68)
                leaver.add_field(
                    name="Leave channel set", value=f"{channel.mention} has been selected if someone left the server")
                await ctx.followup.send(embed=leaver)

            elif type == 'modlog':
                set_modloger(ctx.guild.id, channel.id)

                modlog = Embed(color=0x00FF68)
                modlog.add_field(
                    name="Modlog channel set", value=f"{channel.mention} has been selected to have all moderation actions updated in there.")
                await ctx.followup.send(embed=modlog)

            elif type == 'report_channel':
                set_reporter(ctx.guild.id, channel.id)

                modlog = Embed(color=0x00FF68)
                modlog.add_field(
                    name="Report channel set", value=f"{channel.mention} has been selected to have all reported members in there.")
                await ctx.followup.send(embed=modlog)

    @jeanne_slash(description="Clone a channel")
    @has_permissions(manage_channels=True)
    async def clone(self, ctx: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.news, ChannelType.text, ChannelType.voice, ChannelType.stage_voice]), name=SlashOption(required=False)):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            if name == None:
                name = channel.name

            c = await channel.clone(name=name)

            cloned = Embed(description="{} was cloned as {}".format(
                channel.mention, c.mention))
            await ctx.followup.send(embed=cloned)


def setup(bot: Bot):
    bot.add_cog(slashmanage(bot))