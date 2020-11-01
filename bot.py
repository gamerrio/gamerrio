from discord.ext import commands
import discord, chalk
import logging
import requests
import asyncio
import youtube_dl
import json, random 
import praw
from discord.ext.commands import has_permissions, MissingPermissions

bot = commands.Bot(command_prefix=commands.when_mentioned_or("-"))

bot.remove_command('help')

reddit = praw.Reddit(client_id='Your_id', client_secret='Your_Secret', user_agent='windows 10: Meme Scraper (by /u/PotatoLord1207)')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your browser history!"), status=discord.Status.do_not_disturb)

    print('running')
    print (discord.__version__)
    print('guilds bot is in', len(bot.guilds))


@bot.command(description="Pings the bot", brief="usage !ping")
async def ping(ctx):
    ping_ = bot.latency
    ping = round(ping_ * 1000)
    embed = discord.Embed(
        colour = discord.Colour.orange()
        )
    embed.set_author(name='Ping')
    embed.add_field(name=f"My ping is {ping}ms", value=':ping_pong:', inline=False)

    await ctx.channel.send(embed=embed)

@bot.command(description="send the message content", brief="!say message")
async def say(ctx, *, arg):
    embed = discord.Embed(
    colour = discord.Colour.red()
        )
    embed.set_author(name=arg)
    await ctx.send(embed=embed)

@bot.command(description="Adds two number", brief="usage:!add number number")
async def add(ctx, a: int, b: int):
    embed = discord.Embed(
    colour = discord.Colour.red()
        )
    embed.set_author(name="Sum")
    embed.add_field(name='Number sum is ', value=a+b, inline=False)

    await ctx.send(embed=embed)

@bot.command(description="slap someone", brief="usage: !slap @someone")
async def hug(ctx, members: commands.Greedy[discord.Member], *, reason='no reason', client = discord.member):
    hugged = ", ".join(x.name for x in members)
    person = ctx.author

    embed = discord.Embed(
        colour = discord.Colour.red()
        )
    embed.set_author(name='You Just Got Hugged!')
    embed.add_field(name='{} just got ༼ つ ◕_◕ ༽つ by {}'.format(hugged, person), value=':heart:', inline=False)

    await ctx.channel.send(embed=embed)

@bot.command(description="slap someone", brief="usage: !slap @someone")
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason', client = discord.member):
    slapped = ", ".join(x.name for x in members)

    embed = discord.Embed(
        colour = discord.Colour.red()
        )
    embed.set_author(name='slapped!')
    embed.add_field(name='{} just got slapped for {}'.format(slapped, reason), value=':wave:', inline=False)

    await ctx.channel.send(embed=embed)

@bot.command(description="information about bot")
async def info(ctx):
    embed=discord.Embed(title="Owner:", description="Gamerrio#0097", color=0x8e06bb)
    embed.set_author(name="Information:")
    embed.set_thumbnail(url="https://i.pinimg.com/736x/d4/e8/d3/d4e8d3daab9456b8cdd5d08429c73aa9.jpg")
    embed.add_field(name='Host:', value='Raspberry pi', inline=True)
    embed.set_footer(text="================================")
    await ctx.send(embed=embed)

@bot.command(pass_content=True)
async def help(ctx):
    author = ctx.author.mention
    embed = discord.Embed(
        colour = discord.Colour.orange()
        )
    embed.set_author(name='Help')
    embed.add_field(name='!ping', value='Shows Ping', inline=False)
    embed.add_field(name="!slap", value='Slaps a member', inline=False)
    embed.add_field(name='!ban', value='permanently Bans a person', inline=False)
    await ctx.send(author)
    await ctx.channel.send('Here is your help :helmet_with_cross:', embed=embed)

@bot.command(pass_content=True)
async def clear(ctx, amount = 10):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount+ 1):
        messages.append(message)
    await channel.delete_messages(messages)
    embed = discord.Embed(
        colour = discord.Colour.orange()
        )
    embed.set_author(name='done!')
    embed.add_field(name='cleared ', value='messages'+' :thumbsup:', inline=False)

    await ctx.channel.send(embed=embed)

@bot.command()
async def logout(ctx):
    embed = discord.Embed(
        colour = discord.Colour.orange()
        )
    embed.set_author(name='Logged Out!')

    await ctx.channel.send(embed=embed)
    await bot.logout()

@bot.command(pass_content=True)
async def join(ctx):
    author = ctx.message.author
    voice = ctx.message.author.voice.channel
    await voice.connect()

@bot.command(pass_context=True, name="kick")
@has_permissions(ban_members=True)
async def kick(ctx, user: discord.Member = None, reason = None):
    try:
        if user == None or user == ctx.message.author:
            await ctx.send("You cannot kick yourself!")
            return
        if reason == None:
            reason = "No reason at all!"
        message = f":boot: {user} Kicked because of {reason}!"
        await ctx.send(message)
        await user.kick()
    except:
        await ctx.send('but I dont have Permissions')    

@bot.command(pass_context=True,name="ban")
@has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member = None, reason = None):
    if user == None or user == ctx.message.author:
        await ctx.send("You cannot ban yourself!")
        return
    if reason == None:
        reason = "No reason at all!"
    message = f":hammer: Ban Hammer fallen on {user} because of {reason}!"
    await ctx.send(message)
    await user.ban()

@bot.command(pass_context=True)
async def user(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.add_field(name='Account Created on', value=user.created_at)
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.guild.name), description="Here's what I could find.", color=0x00ff00)
    embed.set_author(name="Server info:")
    embed.add_field(name="Name", value=ctx.message.guild.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.guild.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.guild.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.guild.members))
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def play(ctx):
    author =ctx.message.author
    voice = ctx.message.author.voice.channel
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio('test.mp3'), after=lambda e: print('done', e))

@bot.command(pass_context=True)
async def dog(ctx):
        isVideo = True
        while isVideo:
            r = requests.get('https://random.dog/woof.json')
            js = r.json()
            if js['url'].endswith('.mp4'):
                pass
            else:
                isVideo = False
        colours = [0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63, 0xad1457, 0xf1c40f, 0xc27c0e, 0xa84300, 0xe74c3c, 0x992d22, 0x95a5a6, 0x607d8b, 0x979c9f, 0x546e7a]
        col = int(random.random() * len(colours))
        content = [":dog: Don't be sad! This doggy wants to play with you!", "You seem lonely, {0.mention}. Here, have a dog. They're not as nice as cats, but enjoy!".format(ctx.message.author), "Weuf, woof, woooooooooof. Woof you.", "Pupper!", "Meow... wait wrong animal."]
        con = int(random.random() * len(content))
        em = discord.Embed(color=colours[col])
        em.set_image(url=js['url'])
        await ctx.send(content=content[con], embed=em) 

@bot.command(pass_context=True)
async def cat(ctx):

    response = requests.get('https://aws.random.cat/meow')
    data = response.json()

    colours = [0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63, 0xad1457, 0xf1c40f, 0xc27c0e, 0xa84300, 0xe74c3c, 0x992d22, 0x95a5a6, 0x607d8b, 0x979c9f, 0x546e7a]
    col = int(random.random() * len(colours))
    content = [":cat: Don't be sad! This cat wants to play with you!", "You seem lonely, {0.mention}. Here, have a cat. They're not as nice as dog, but enjoy!".format(ctx.message.author), "meow, meow, oooooooooof. meow you.", "Pupper!", "Woof... wait wrong animal."]
    con = int(random.random() * len(content))
    em = discord.Embed(color=colours[col])
    em.set_image(url=data['file'])
    await ctx.send(content=content[con], embed=em)

@bot.command()
async def meme(ctx):
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 30)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    embed = discord.Embed(title="Memes", description="Here is the Your Meme", color=0x00ff00)
    embed.set_image(url=submission.url)    
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def userpic(ctx, user:discord.Member):
    embed = discord.Embed(title="{}'s Picture".format(user.name), description="Here is the User Profile Picture", color=0x00ff00)
    embed.set_image(url=user.avatar_url)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def guess(ctx):
    embed = discord.Embed(title="Guess a Number", description='Between 1 to 10',colour=0x00ff00)
    await ctx.send(embed=embed)

    def guess_check(m):
        return m.content.isdigit()

    guess = await bot.wait_for('message', timeout=5.0, check=guess_check)
    answer = random.randint(1,10)
    if guess is None:
        embed = discord.Embed(title="Sorry, It was", description='{}'.format(answer),colour=0x00ff00)
        await ctx.send(embed=embed)
        return
    if int(guess.content) == answer:
        embed = discord.Embed(title="You are right", description=':tada: it is {}'.format(answer),colour=0x00ff00)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Sorry, It was", description='{}'.format(answer),colour=0x00ff00)
        embed.set_thumbnail(url='https://cdn.shopify.com/s/files/1/1061/1924/products/Very_sad_emoji_icon_png_large.png?v=1480481019')
        await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def face(ctx):
    async with ctx.typing():
        await ctx.send('( ͡° ͜ʖ ͡°)')

@bot.command(pass_context=True)
async def moonwalk(ctx):
    async with ctx.typing():
       m1 = await ctx.send(".:walking:")    
       l = [":runner:",":walking:"]
       t = "."
       for i in range(25):
          t = t + "."
          s = t+l[i%2]
          await m1.edit(content=s)

bot.run("token")
