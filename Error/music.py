import discord
import datetime

async def out_of_vc(ctx, text=None):
    embed = discord.Embed(
        title="Error :red_circle:",
        description=text,
        color=discord.Color.from_rgb(204, 0, 0)
    ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

    return await ctx.reply(embed = embed)

def video_time(time):
    conversion = datetime.timedelta(seconds=time)
    return str(conversion)

def views(views):
    numbers = list(str(views))
    numbers.reverse()

    increased = 0
    changed = False

    for index in range(0, len(numbers)):
        if ((index+increased) % 2 == 0) and ((index+increased) != 0) and ((index+increased) != len(numbers)-1) and (not changed):
            numbers.insert((index+increased)+1, " ")
            increased += 1
            changed = True

        elif changed != False:
            changed = False

    numbers.reverse()
    return "".join(numbers)

async def song_message(ctx, song, title, suggested=False):
    embed = discord.Embed(
        title=title,
        color=discord.Color.from_rgb(253, 10, 37)
    ).set_thumbnail(url=song.thumbnail)

    if suggested:
        embed.set_footer(text=f"Suggested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.set_author(name=song.channel, url=song.channel_url)
    embed.description = f"[{song.name}]({song.url})"
    embed.add_field(name="__Duration__", value="{}".format(f"**```{video_time(song.duration)}```**" if song.duration != 0 else ':heart_on_fire:**Live Now**'), inline=True)
    embed.add_field(name="__Views__", value=f"**```{views(song.views)}```**", inline=True)
    #embed.add_field(name="👍 __Likes__", value=f"**```{song.likes}```**", inline=True)

    return await ctx.reply(embed=embed)

async def get_queue_embed(ctx, queue:list=None):
    embed = discord.Embed(title='Queue :dvd: ', color=discord.Color.from_rgb(253, 10, 37))
    embed.description = "\n".join(song.name for song in queue) if (queue != None and queue != []) else "**```Queue is empty!```**"
    return await ctx.reply(embed=embed)