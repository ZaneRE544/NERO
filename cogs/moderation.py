from discord import User, Member, Embed, NotFound
from re import findall, compile
from asyncio import sleep
from discord.ext.commands import MissingPermissions, command as jeanne, Cog, Converter, BadArgument, has_permissions as perms, bot_has_permissions as bot_perms
from discord.ext.commands.errors import MemberNotFound
from discord.utils import get


time_regex = compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}

class TimeConverter(Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise BadArgument(
                    "{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise BadArgument("{} is not a number!".format(v))
        return time


class moderation(Cog):
    def __init__(self, bot):
        self.bot = bot

    @jeanne(aliases=['unb'])
    @perms(ban_members=True)
    async def unban(self, ctx, user : User, *, reason=None):
        await ctx.guild.unban(user)
        embed = Embed(title="User Unbanned", color=0xFF0000)
        embed.add_field(name="Member",
                        value=f"**>** **Name:** {user}\n**>** **ID:** {user.id}",
                        inline=True)
        embed.add_field(
            name="Moderation", value=f"**>** **Responsible Moderator:** {ctx.author}\n**>** **Reason:** {reason}", inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = Embed(
                title="Unban failed", description="Sorry but you cannot unban this user", color=0xff0000)
            embed.add_field(
                name="Reason", value="Missing permissions: Ban Members", inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, MemberNotFound):
            embed = Embed(
                title="Unban failed", description="Invalid user ID given.", color=0xff0000)
            await ctx.send(embed=embed)

    @jeanne()
    @perms(kick_members=True)
    async def unmute(self, ctx, member: Member):
        mutedRole = get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        unmute = Embed(
            title="Member Unmute", color=0xFF0000)
        unmute.add_field(name="Member",
                        value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                        inline=True)
        unmute.add_field(
            name="Moderation", value=f"**>** **Responsible Moderator:** {ctx.author}", inline=True)
        unmute.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=unmute)

    @jeanne(pass_context=True, aliases=['w'])
    @perms(kick_members=True)
    async def warn(self, ctx, member: Member, reason=None):
        if reason == None:
            reason = "Unspecified"
        warn = Embed(title="Member warned", color=0xFF0000)
        warn.add_field(name="Member",
                        value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                        inline=True)
        warn.add_field(
            name="Moderation", value=f"**>** **Responsible Moderator:** {ctx.author}\n**>** **Reason:** {reason}", inline=True)
        warn.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=warn)

    @warn.error
    async def warn_error(self, ctx, error):
             if isinstance(error, MissingPermissions):
                embed=Embed(title="Warn failed", description="Sorry but you cannot warn this user", color=0xff0000)
                embed.add_field(name="Reason", value="Missing permissions: Kick Members", inline=False)
                await ctx.send(embed=embed)



    @jeanne(aliases=['b'])
    @perms(ban_members=True)
    async def ban(self, ctx, user: User, *, reason=None):
        guild = ctx.guild
        if reason == None:
            reason = "Unspecified"

        try:
            banned = await guild.fetch_ban(user)
        except NotFound:
            banned = False

        if banned:
            already_banned = Embed(description="User is already banned here")
            await ctx.send(embed=already_banned)
        
        else:
            try:
                banmsg = Embed(
                    description=f"You are banned from **{ctx.guild.name}** for **{reason}**")
                await user.send(embed=banmsg)
            except:
                pass
            ban = Embed(title="Member Banned", color=0xFF0000)
            ban.add_field(name="Member",
                        value=f"**>** **Name:** {user}\n**>** **ID:** {user.id}",
                        inline=True)
            ban.add_field(
                name="Moderation", value=f"**>** **Responsible Moderator:** {ctx.author}\n**>** **Reason:** {reason}", inline=True)
            ban.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=ban)
            await guild.ban(user, reason=reason)


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed=Embed(title="Ban failed", description="Sorry but you cannot ban this user", color=0xff0000)
            embed.add_field(name="Reason", value="Missing permissions: Ban Members", inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, MemberNotFound):
            embed = Embed(
                title="Ban failed", description="Invalid user ID given.", color=0xff0000)
            await ctx.send(embed=embed)
            
   

    @jeanne(aliases=['k'])
    @perms(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason=None):
        guild=ctx.guild
        try:
            kickmsg = Embed(
                description=f"You are kicked from **{ctx.guild.name}** for **{reason}**")
            await member.send(embed=kickmsg)
        except:
            pass
        kick = Embed(title="Member Kicked", color=0xFF0000)
        kick.add_field(name="Member",
                       value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                       inline=True)
        kick.add_field(
            name="Moderation", value=f"**>** **Responsible Moderator:** {ctx.author}\n**>** **Reason:** {reason}", inline=True)
        kick.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=kick)
        await guild.kick(member, reason=reason)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed=Embed(title="Kick failed", description="Sorry but you cannot kick this user", color=0xff0000)
            embed.add_field(name="Reason", value="Missing permissions: Kick Members", inline=False)
            await ctx.send(embed=embed)
   
        
    @jeanne()
    @bot_perms(manage_roles=True)
    async def muterole(self, ctx):
        guild=ctx.guild
        await guild.create_role(name="Muted")
        await ctx.send("Mute role created")


        for channel in guild.channels:
                mute_role=get(guild.roles, name="Muted")
                await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        

    @jeanne()
    @perms(kick_members=True)
    async def mute(self, ctx, member: Member, time: TimeConverter = None, *, reason=None):
        guild = ctx.guild
        mutedRole = get(guild.roles, name="Muted")

        await member.add_roles(mutedRole)
        mute = Embed(title="Member Muted", color=0xff0000)
        mute.add_field(name="Member",
                       value=f"**>** **Name:** {member}\n**>** **ID:** {member.id}",
                       inline=True)
        mute.add_field(
            name="Moderation", value=f"**>** **Responsible Moderator:** {ctx.author}\n**>** **Reason:** {reason}\n**>** **Duration:** {time}", inline=True)
        mute.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=mute)
        if time:
            await sleep(time)
            await member.remove_roles(mutedRole)
        
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed=Embed(title="Mute failed", description="Sorry but you cannot mute this user", color=0xff0000)
            embed.add_field(name="Reason", value="Missing permissions: Kick Members", inline=False)
            await ctx.send(embed=embed)     

 
    @jeanne(aliases=['nick', 'changenick', 'setnick'])
    @perms(manage_nicknames=True)
    async def change_nickname(self, ctx, member: Member, *, nickname=None):

        if not nickname:
            nonick = Embed(description="Please add a nickname")
            await ctx.send(embed=nonick)

        else:
            await member.edit(nick=nickname)
            setnick = Embed(color=0x00FF68)
            setnick.add_field(name="Nickname changed",
                        value=f"{member}'s nickname is now `{nickname}`", inline=False)
            await ctx.send(embed=setnick)

    @change_nickname.error
    async def change_nickname_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = Embed(
                title="Change Nickname failed", description="Sorry but you cannot change this member's nickname", color=0xff0000)
            embed.add_field(
                name="Reason", value="Missing permissions: Manage Nicknames", inline=False)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(moderation(bot))
