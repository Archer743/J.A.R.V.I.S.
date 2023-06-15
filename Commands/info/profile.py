import discord
from discord.ext import commands

from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

import time, datetime
from io import BytesIO
from PIL import Image, ImageChops, ImageDraw, ImageFont
from random import randint

from sys import path
path.insert(1, "../../Data")
from Data.DB_commands.bot_info import increase_uses


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    def circle(self, pfp, size = (215,215)):
        pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
        
        bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(pfp.size, Image.ANTIALIAS)
        mask = ImageChops.darker(mask, pfp.split()[-1])
        pfp.putalpha(mask)
        return pfp


    @cog_ext.cog_slash(
        name="profile",
        description="Provides member's info",
        guild_ids=[805867479909924905],
        options=[
            create_option(
                name="type",
                description="Select my answer's format",
                required=True,
                option_type=3,
                choices=[
                    create_choice(name="txt format", value="txt"),
                    create_choice(name="png format", value="png")
                ]
            ),
            create_option(
                name="member",
                description="Select one member",
                required=True,
                option_type=6
            )
        ]
    )
    async def profile(self, ctx:SlashContext, type:str, member:discord.Member):
        if type == "png":
            name, nick, Id, status = str(member), member.display_name, str(member.id), str(member.status).upper()

            created_at = member.created_at.strftime("%a, %#d %B %Y")
            created_at_clock = member.created_at.strftime("%I:%M %p, UTC")

            joined_at = member.joined_at.strftime("%a, %#d %B %Y")
            joined_at_clock = member.joined_at.strftime("%I:%M %p, UTC")

            base = Image.open("./Commands/Templates/base.png").convert("RGBA")
            background = Image.open(f"./Commands/Templates/{randint(1, 10)}.png").convert("RGBA")
            
            member_image = member.avatar_url_as(size=256)
            data = BytesIO(await member_image.read())
            member_image = Image.open(data).convert("RGBA")
            
            name = f"{name[:16]}.." if len(name)>16 else name
            nick = f"AKA - {nick[:17]}.." if len(nick)>17 else f"AKA - {nick}"

            draw = ImageDraw.Draw(base)
            member_image = self.circle(member_image, size=(215, 215))

            font = ImageFont.truetype("./Commands/TTF_files/Nunito-Regular.ttf", 38)
            akafont = ImageFont.truetype("./Commands/TTF_files/Nunito-Regular.ttf", 30)
            subfont = ImageFont.truetype("./Commands/TTF_files/Nunito-Regular.ttf", 25)
                        # x     y
            draw.text((280, 240), name, font=font)
            draw.text((270, 315), nick, font=akafont)
            draw.text((65, 490), Id, font=subfont)
            draw.text((405, 490), status, font=subfont)
            draw.text((75, 613), created_at, font=subfont)
            draw.text((75, 650), created_at_clock, font=subfont)
            draw.text((405, 613), joined_at, font=subfont)
            draw.text((405, 650), joined_at_clock, font=subfont)

            base.paste(member_image, (56, 158), member_image)
            background.paste(base, (0, 0), base)

            with BytesIO() as a:
                background.save(a, "PNG")
                a.seek(0)
                await ctx.reply(file = discord.File(a, "profile.png"))
                increase_uses()

        elif type == "txt":
            embed=discord.Embed(color=member.top_role.color)
            embed.set_thumbnail(url=member.avatar_url)

            status_text, status_title = "", ""
            if str(member.raw_status) == "dnd":
                status_text = "Do Not Disturb"
                status_title = "Status :red_circle:"
            elif str(member.raw_status) == "idle":
                status_text = "Idle"
                status_title = "Status :crescent_moon:"
            elif str(member.raw_status) == "online":
                status_text = "Online"
                status_title = "Status :green_circle:"
            else:
                status_text = "Offline"
                status_title = "Status :white_circle:"

            embed.add_field(name="Username", value=f"```{member}```", inline=True)
            embed.add_field(name=f"{status_title}", value=f"```{status_text}```", inline=True)
            embed.add_field(name="Roles", value=f"```{len(member.roles)}```", inline=True)

            embed.add_field(name="Nickname (AKA)", value=f"```{member.nick}```", inline=True)
            embed.add_field(name="Bot?", value=f"```{member.bot}```", inline=True)
            embed.add_field(name="Top Role", value=f"{member.top_role.mention}", inline=True)

            embed.add_field(name=f"Created At", value="```{}```".format(member.created_at.strftime("%a, %#d %B %Y, %I:%M %p, UTC")), inline=True)
            embed.add_field(name=f"Joined At", value="```{}```".format(member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p, UTC")), inline=True)
            embed.add_field(name="ID", value=f"```{member.id}```", inline=True)

            await ctx.reply(embed=embed)
            increase_uses()
   

def setup(client):
    client.add_cog(Profile(client))