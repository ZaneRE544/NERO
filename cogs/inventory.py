from typing import Optional
from assets.buttons import Confirmation
from db_functions import add_user_custom_wallpaper, add_user_wallpaper, check_botbanned_user, fetch_user_inventory, fetch_wallpapers, get_balance, create_user_inventory, get_wallpaper, use_wallpaper
from discord import *
from discord.ext.commands import Cog, Bot, GroupCog
from assets.generators.level_card import Level
from asyncio import get_event_loop
from functools import partial
import requests


class Shop_Group(GroupCog, name="shop"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()
        
    @app_commands.command(description="Check all the wallpapers available")
    async def backgrounds(self, ctx: Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            qp = self.bot.get_emoji(980772736861343774)
            await ctx.followup.send(embed=fetch_wallpapers(qp))

class Background_Group(GroupCog, name="background"):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()
    
    def get_card(self, args):
        image = Level().generate_level(**args)
        return image
    
    @app_commands.command(description="Preview the background image")
    async def preview(self, ctx: Interaction, item_id:str):
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            await ctx.response.defer()
            qp = self.bot.get_emoji(980772736861343774)
            wallpaper = get_wallpaper(item_id)
            embed = Embed(title="Preview backgorund")
            embed.color = ctx.user.color
            embed.add_field(name="Name", value=wallpaper[1], inline=True)
            embed.add_field(name="Price", value=f"1000 {qp}", inline=True)
            embed.set_image(url=wallpaper[2])
            await ctx.followup.send(embed=embed)
    
    @app_commands.command(description="Buy a background pic for your level card")
    async def buy(self, ctx:Interaction, item_id:str):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            balance:int = get_balance(ctx.user.id)
            
            if balance == 0:
                nomoney = Embed(description='You have no QP.\nPlease get QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.followup.send(embed=nomoney)
            
            elif balance < 1000:
                notenough = Embed(
                    description='You do not have enough QP.\nPlease get more QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.followup.send(embed=notenough)

            else:
                qp = self.bot.get_emoji(980772736861343774)
                wallpaper=get_wallpaper(item_id)
                        
                if wallpaper == None:
                    nonexist=Embed(description='Invalid item ID passed')
                    await ctx.followup.send(embed=nonexist)

                else:
                    args = {
                        'level_card': wallpaper[2],
             	    	'profile_image': str(ctx.user.avatar.with_format('png')),
     			        'server_level': 100,
     			        'server_user_xp': 50,
     			        'server_next_xp': 100,
                        'global_level': 100,
     			        'global_user_xp': 100,
     			        'global_next_xp': 100,
     			        'user_name': str(ctx.user),
                        }

                    func = partial(self.get_card, args)
                    image = await get_event_loop().run_in_executor(None, func)

                    file = File(fp=image, filename=f'preview_level_card.png')

                    preview=Embed(description="This is the preview of the level card.", color=Color.blue()).add_field(name="Cost", value=f"{wallpaper[3]} {qp}").set_footer(text="Is this the background you wanted?")
                    view=Confirmation()
                    await ctx.followup.send(file=file, embed=preview, view=view)
                    await view.wait()

                    if view.value == None:
                        await ctx.edit_original_response(content="Timeout", view=None, embed=None)
                    elif view.value is True:
                        if create_user_inventory(ctx.user.id) == False:
                            pass
                        add_user_wallpaper(ctx.user.id, item_id)
                        embed1 = Embed(description=f"Background wallpaper bought and selected",color=Color.blue())
                        await ctx.edit_original_response(embed=embed1, view=None)

                    elif view.value is False:
                        await ctx.edit_original_response("Cancelled", view=None, embed=None)

    @app_commands.command(description='Select a wallpaper')
    async def use(self, ctx: Interaction, name: str):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            user_inv = fetch_user_inventory(ctx.user.id)

            if f'{name}.png' in user_inv:
                use_wallpaper(name, ctx.user.id)
                embed = Embed(
                    description=f"{name} has been selected", color=ctx.user.color)
                await ctx.followup.send(embed=embed)
            else:
               embed = Embed(
                   description="This background image is not in your inventory", color=Color.red())
               await ctx.followup.send(embed=embed)

    @app_commands.command(description="Buy a custom background pic for your level card")
    async def buycustom(self, ctx: Interaction, name: str, link: Optional[str]=None, image:Optional[Attachment]=None) -> None:
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            balance = get_balance(ctx.user.id)

            if balance == None:
                nomoney = Embed(
                    description='You have no QP.\nPlease get QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.followup.send(embed=nomoney)

            elif int(balance) < 1000:
                notenough = Embed(
                    description='You do not have enough QP.\nPlease get more QP by doing `/daily`, `/guess` and/or `/dice`')
                await ctx.followup.send(embed=notenough)
            
            elif link and image:
                one = Embed(
                    description="Please use either an image URL or image")
                await ctx.followup.send(embed=one)

            else:

                alert = """
Before you buy a custom background picture, did you make sure the image is:

    1. A valid image/image URL
    2. Not crossing NSFW borderline
    3. Does not contain any lewded characters and/or lolis
    4. Is not sexualised in some way
    5. Does not violate ToS and/or contains TW slurs
    6. The name you set for it also does not violate ToS and/or contains TW slurs
    7. The image's resolution is at a 9:5 ratio and at least 900x500 for better quality.

If you feel that the image fits the above or not, click one of the buttons to continue
"""
                view = Confirmation()
                confirm = Embed(description=alert, color=ctx.user.color)
                await ctx.followup.send(embed=confirm, view=view)
                await view.wait()
                if view.value == True:
                    loading = self.bot.get_emoji(1012677456811016342)
                    await ctx.edit_original_response(content="Creating preview... This will take some time {}".format(loading), view=None, embed=None)
                    qp = self.bot.get_emoji(980772736861343774)
                    if requests.get(link).status_code == 200:

                        if image:
                            link=image.url
                        args = {'level_card': link, 'profile_image': str(ctx.user.avatar.with_format('png')), 'server_level': 100, 'server_user_xp': 50, 'server_next_xp': 100, 'global_level': 100, 'global_user_xp': 100, 'global_next_xp': 100, 'user_name': str(ctx.user),}

                        func = partial(self.get_card, args)
                        image = await get_event_loop().run_in_executor(None, func)

                        file = File(fp=image, filename='preview_level_card.png')

                        preview = Embed(description="This is the preview of the level card.", color=Color.blue()).add_field(name="Cost", value=f"1000 {qp}").set_footer(text="Is this the background you wanted?").set_footer(text="Please note that if the custom background violates ToS or is NSFW, it will be removed with NO REFUNDS!")
                        view = Confirmation()
                        await ctx.edit_original_response(content=None, attachments=[file], embed=preview, view=view)
                        await view.wait()

                        if view.value is None:
                            await ctx.edit_original_response(content="Time out", view=None)
                        elif view.value is True:
                            add_user_custom_wallpaper(ctx.user.id, name, link)

                            embed1 = Embed(
                                description=f"Background wallpaper bought and selected.", color=Color.blue())
                            await ctx.edit_original_response(embed=embed1, view=None)

                        elif view.value is False:
                            await ctx.edit_original_response(content="Cancelled", embed=None, view=None)
                elif view.value == False:
                    check = Embed(
                        description="Please try to sort out the image first and try again", color=Color.blue())
                    await ctx.edit_original_response(view=None, embed=check)
                elif view.value == None:
                    await ctx.edit_original_response(content="Time out", embed=None, view=None)

    @app_commands.command(description='Check which backgrounds you have')
    async def list(self, ctx: Interaction):
        await ctx.response.defer()
        if check_botbanned_user(ctx.user.id) == True:
            pass
        else:
            try:
                a = fetch_user_inventory(ctx.user.id)
                inv = Embed(title="List of wallpapers you have",
                            color=Color.blue())
                inv.description = a
                await ctx.followup.send(embed=inv)
            except FileNotFoundError:
                embed = Embed(
                    description="Your inventory is empty", color=Color.red())
                await ctx.followup.send(embed=embed)
              
async def setup(bot:Bot):
    await bot.add_cog(Shop_Group(bot))
    await bot.add_cog(Background_Group(bot))