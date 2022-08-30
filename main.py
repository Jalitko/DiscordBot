from discord.ext import commands
import discord
from time import sleep
import datetime
import asyncio
import os
import logging

from vars import *
from defs import *

bot = commands.Bot(command_prefix = "?")



logging.basicConfig(filename = "logfile.log",
                    filemode = "a",
                    format = "%(levelname)s %(asctime)s - %(message)s", 
                    level = 40)
logger = logging.getLogger()


@bot.event
async def on_ready():
    print(f"Bot is running  {discord.__version__}")
    await bot.change_presence(activity=discord.Game(name = default_activity))



"""
 $$$$$$\  $$$$$$$$\ $$\   $$\ $$$$$$$$\ $$$$$$$\   $$$$$$\  $$\       
$$  __$$\ $$  _____|$$$\  $$ |$$  _____|$$  __$$\ $$  __$$\ $$ |      
$$ /  \__|$$ |      $$$$\ $$ |$$ |      $$ |  $$ |$$ /  $$ |$$ |      
$$ |$$$$\ $$$$$\    $$ $$\$$ |$$$$$\    $$$$$$$  |$$$$$$$$ |$$ |      
$$ |\_$$ |$$  __|   $$ \$$$$ |$$  __|   $$  __$$< $$  __$$ |$$ |      
$$ |  $$ |$$ |      $$ |\$$$ |$$ |      $$ |  $$ |$$ |  $$ |$$ |      
\$$$$$$  |$$$$$$$$\ $$ | \$$ |$$$$$$$$\ $$ |  $$ |$$ |  $$ |$$$$$$$$\ 
 \______/ \________|\__|  \__|\________|\__|  \__|\__|  \__|\________|
"""



@bot.event
async def on_message(ctx):
    if bot.user.mentioned_in(ctx) and "<@!710901098860511252>" in ctx.content:    
        await ctx.channel.purge(limit = 1)

        data = read()
        id = str(ctx.guild.id)

        room = data[id][0]["room"]
        move = data[id][0]["move"]
        prefix = data[id][0]["prefix"]
        roles = data[id][0]["roles"]
        room_name = bot.get_channel(room)

        if move: move = "yes"
        else: move = "no"

        roles = ', '.join(roles)

        description = f"""
        INFO:
        Timeout room: {room_name}
        Moving: {move}
        Prefix: {prefix}
        Roles: {roles}

        COMMANDS:
        {prefix}move <username>
        {prefix}stop
        {prefix}room <channel>
        {prefix}roles <role>;<role>...
        """

        embed=discord.Embed(description=description, color=0xFF5733)

        await ctx.channel.send(embed = embed)

    

    await bot.process_commands(ctx)



@bot.command()
async def move(ctx,*, member: discord.Member):
    await ctx.channel.purge(limit = 1)
    if not inroles(ctx.guild.id, ctx.author.roles): return 0
        
    data = read()

    server_id =     ctx.guild.id
    channel_id =    data[str(server_id)][0]["room"]
    mulitple =      data[str(server_id)][0]["multiple"]
    data[str(server_id)][0]["move"] = True

    channel = discord.utils.get(ctx.guild.voice_channels, id=channel_id)
    await bot.change_presence(activity=discord.Game(name = timeout_activity))

    a = False

    if not mulitple:
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio(song), after=lambda e: print('done'))
        a = True
        data[str(server_id)][0]["multiple"] = True
    
    write(data)


    
    while ismove(server_id):    
        try:    await member.move_to(channel)
        except: pass
        sleep(0.5)

    await bot.change_presence(activity=discord.Game(name = default_activity))
    data = read()
    data[str(server_id)][0]["multiple"] = False
    write(data)

    if a: 
        vc.stop()
        await vc.disconnect()

        

@bot.command()
async def stopmoving(ctx):
    await ctx.channel.purge(limit = 1)
    if not inroles(ctx.guild.id, ctx.author.roles): return 0
    
    print(False)
    server_id = ctx.guild.id

    data = read()
    data[str(server_id)][0]["move"] = False
    write(data)




    
@bot.command()
@commands.has_permissions(administrator=True)
async def room(ctx,*, name_channel):
    await ctx.channel.purge(limit = 1)

    print(name_channel)
    server_id = ctx.guild.id
    channel = discord.utils.get(ctx.guild.channels, name=name_channel)
    channel = channel.id
    print(channel)
    
    data = read()

    try:    data[str(server_id)][0]["room"] = channel
    except: data[server_id] = [{"room": channel, "move": "False", "multiple": "False", "prefix": "?", "roles": ["@everyone"]}]

    write(data)



@bot.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx,p):
    await ctx.channel.purge(limit = 1)
    
    data = read()
    id = str(ctx.guild.id)
    data[id][0]["prefix"] = p
    write(data)


@bot.command()
@commands.has_permissions(administrator=True)
async def roles(ctx,*,roles):
    await ctx.channel.purge(limit = 1)
    
    data = read()
    id = str(ctx.guild.id)

    roles = roles.split(';')
    
    data[id][0]["roles"] = roles
    
    write(data)




"""
 $$$$$$\   $$$$$$\  $$\    $$\ $$$$$$\ $$$$$$$\  
$$  __$$\ $$  __$$\ $$ |   $$ |\_$$  _|$$  __$$\ 
$$ /  \__|$$ /  $$ |$$ |   $$ |  $$ |  $$ |  $$ |
$$ |      $$ |  $$ |\$$\  $$  |  $$ |  $$ |  $$ |
$$ |      $$ |  $$ | \$$\$$  /   $$ |  $$ |  $$ |
$$ |  $$\ $$ |  $$ |  \$$$  /    $$ |  $$ |  $$ |
\$$$$$$  | $$$$$$  |   \$  /   $$$$$$\ $$$$$$$  |
 \______/  \______/     \_/    \______|\_______/
"""




async def covid_bot():
    await bot.wait_until_ready()
    channel = bot.get_channel(id = covid_chnnel)
    
    pcr_test_path = '//*[@id="block_603780b691b98"]/div/h2/text()'
    pcr_pos_path =  '//*[@id="block_6037862491b9a"]/div/h2/text()'

    ag_test_path = '//*[@id="block_60378ba2c4f83"]/div/h2/text()'
    ag_pos_path = '//*[@id="block_60378c0bc4f85"]/div/h2/text()'

    dead_path = '//*[@id="block_60378d5bc4f89"]/div/h2/text()'
    hospitalized_path = '//*[@id="block_60378c91c4f87"]/div/h2/text()'
    hospitalized_total_path = '//*[@id="block_5e9f60f747a89"]/div/h3/text()'
    
    
    while not bot.is_closed():

        try:
            date = datetime.datetime.now().strftime('%x')
            last_date = open(last_date_txt, "r").read()
            last_num = open(last_num_txt, "r").read()
            hospitalized_total_last = open(hospitalized_txt, "r").read()
            

            if date != last_date and int(positive(pcr_test_path)) != int(last_num):

                pcr_test = positive(pcr_test_path)
                pcr_pos = positive(pcr_pos_path)

                ag_test = positive(ag_test_path)
                ag_pos = positive(ag_pos_path)

                deaths = positive(dead_path)
                hospitalized = positive(hospitalized_path)
                hospitalized_total = positive(hospitalized_total_path)

                # if hospitalized_total >= hospitalized_total_last: plus_minus = ''
                # else: plus_minus = ''
                
                x = datetime.datetime.now().strftime("%x")

                text = f"PCR test: {format_int(pcr_test)}\nPCR pos.: {format_int(pcr_pos)}\nAG test: {format_int(ag_test)}\nAG pos.: {format_int(ag_pos)}\nHospitalized: {hospitalized_total}\nDeaths: {deaths}\n{x}"

                title = f'COVID-19 {emote_Pepehands}{emote_covid}'
                write_data(last_date_txt, date)
                write_data(last_num_txt, pcr_test)
                write_data(hospitalized_txt, hospitalized_total)

                embed=discord.Embed(title=title, description=text, color=0xFF5733)

                await channel.send(embed = embed)

        except Exception as e: 
            print(e)
            pass
        
        await asyncio.sleep(60)





"""
 $$$$$$\  $$$$$$$\ $$\     $$\ $$$$$$$\ $$$$$$$$\  $$$$$$\  
$$  __$$\ $$  __$$\\$$\   $$  |$$  __$$\\__$$  __|$$  __$$\ 
$$ /  \__|$$ |  $$ |\$$\ $$  / $$ |  $$ |  $$ |   $$ /  $$ |
$$ |      $$$$$$$  | \$$$$  /  $$$$$$$  |  $$ |   $$ |  $$ |
$$ |      $$  __$$<   \$$  /   $$  ____/   $$ |   $$ |  $$ |
$$ |  $$\ $$ |  $$ |   $$ |    $$ |        $$ |   $$ |  $$ |
\$$$$$$  |$$ |  $$ |   $$ |    $$ |        $$ |    $$$$$$  |
 \______/ \__|  \__|   \__|    \__|        \__|    \______/ 
"""




async def crypto_bot():
    await bot.wait_until_ready()
    channel = bot.get_channel(id = crypto_channel)
    
    while not bot.is_closed():
        try:
            last_date = open(last_date_crpyto, "r").read()
            date = datetime.datetime.now().strftime('%x')
            time = int(datetime.datetime.now().strftime('%H'))
            
            if date != last_date and time >= 10:
                prices = get_prices(coins)
                lines = []
                total_price = []

                for i,coin in coins.items():
                    emote = coin["emote"]
                    price = prices[0][i]
                    name = coin["short"]
                    toshort = coin["toshort"]

                    lines.append(f"{emote} **{name}**: {format_float(price)}{toshort} _({percentage_str(prices, i)})_")
                    total_price.append(percentage_float(prices, i))

                
                if sum(total_price) > 0: x = 1
                else: x = 0
                color = [0xFF5733, 0x00FF00]


                text = '\n'.join(map(str, lines))
                title = f"Crypto {emote_cryptotitle[x]}"
                embed=discord.Embed(title=title,description=text, color=color[x])

                await channel.send(embed = embed)
                
                write_data(last_date_crpyto, date)


        except Exception as e: 
            print(e)
            pass
        
        await asyncio.sleep(5)




@bot.command(aliases= [c["short"].lower() for i,c in coins.items()])
async def crypto_now(ctx, chart = "not"):
    coin = ctx.invoked_with.upper()
    
    author = str(ctx.author).split("#")[0]

    index = 0
    for i,c in coins.items():
        if c["short"] == str(coin):
            index = i
            continue
    price = get_prices({index: coins[index]})
    
    
    percentage = percentage_str(price, 0)
    price = format_float(price[0][0])

    if "Direct Message" in str(ctx.message.channel):
        color = coins[index]["color"]
        emote = coins[index]["emote"]
        to = coins[index]["toshort"]
        title = f"Aktuálna cena digitálnych peniažkov"
        text = f'{emote} **{coin}**: {price}{to} _({percentage})_'
        

        embed=discord.Embed(title=title,description=text, color=color)
        
        logger.error(f"{author}: {coin} {chart}")

        if chart == "chart":
            coins_chart(index)
            file = discord.File("chart.png")
            embed.set_image(url="attachment://chart.png")


            await ctx.send(embed = embed, file=file)  
            os.remove("chart.png")
        else: 
            await ctx.send(embed = embed)

    else:
        await ctx.channel.purge(limit = 1)
        
@bot.command()
async def printemote(ctx):
    context = ctx.message.content
    symebols = ["<", ">", ":"]
    for i in symebols: context = context.replace(i, "")
    await ctx.send(context)
    




"""
$$\      $$\ $$\   $$\  $$$$$$\  $$$$$$\  $$$$$$\  
$$$\    $$$ |$$ |  $$ |$$  __$$\ \_$$  _|$$  __$$\ 
$$$$\  $$$$ |$$ |  $$ |$$ /  \__|  $$ |  $$ /  \__|
$$\$$\$$ $$ |$$ |  $$ |\$$$$$$\    $$ |  $$ |      
$$ \$$$  $$ |$$ |  $$ | \____$$\   $$ |  $$ |      
$$ |\$  /$$ |$$ |  $$ |$$\   $$ |  $$ |  $$ |  $$\ 
$$ | \_/ $$ |\$$$$$$  |\$$$$$$  |$$$$$$\ \$$$$$$  |
\__|     \__| \______/  \______/ \______| \______/ 
"""




from discord.utils import get
from discord import FFmpegPCMAudio
from pytube import YouTube
import discord
song_list = {}



@bot.command(aliases=["p", "paly"])
async def play(ctx, *, url = "https://youtu.be/4TLk42qPa60"):
    #url = "https://www.youtube.com/watch?v=vkpYIvL_B5I"
    #if url == "2": url = "MREEK FC'ED ORIGINAL UNITED WITH DT"

    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    
    if ("youtube.com" or "youtu.be") not in url:
        url = title_to_url(url)
    
    
    files = os.listdir('C:/vs/dc/corner/songs')

    yt = YouTube(url)
    stream = yt.streams.get_by_itag(18)
    video_length = f"[{time_length(yt.length)}]"
    title_time = f"{stream.title} {video_length}"
    better_title = delete_symbols(stream.title)

    for file in files:
        a = file.split(".")[0]

        if a == better_title:
            break
        else:
            stream.download("C:/vs/dc/corner/songs")

    song_path = f"songs/{better_title}.mp4"
    source = FFmpegPCMAudio(song_path)

    try:
        song_list[ctx.guild.id][0].append(source)
        song_list[ctx.guild.id][1].append(title_time)
        song_list[ctx.guild.id][2].append(song_path)
    except:
        song_list[ctx.guild.id] = [[source], [title_time], [song_path], False]


    queued = len(song_list[ctx.guild.id][1])
    if queued == 1: title = f"Now playing"
    else: title = f"Track queued - Position {queued-1}"
    
    text = f'{stream.title}'
    embed=discord.Embed(title=title,description=text, color=0xff0000)
    await ctx.send(embed = embed)


    if len(song_list[ctx.guild.id][0]) == 1: await start_playing(ctx,voice)
    print(f"{ctx.guild.name}: {song_list[ctx.guild.id][1]}")


async def start_playing(ctx, voice):
    print(f"{ctx.guild.name}: {song_list[ctx.guild.id][1]}")
    
    i = 0
    #while len(song_list[ctx.guild.id][0]) > 0:
    while i <60:
        await asyncio.sleep(1)
        if len(song_list[ctx.guild.id][0]) == 0: i+=1
        else: i = 0

        if voice.is_paused(): continue
        
        try:
            source = song_list[ctx.guild.id][0][0]
            voice.play(source, after=lambda e:check_queue(ctx.guild.id, song_list[ctx.guild.id][3]))

        except Exception as e: 
            #print(e)
            continue
    await voice.disconnect()
  

def check_queue(id, loop, n=1):

    if loop:
        song_list[id][0][0] = FFmpegPCMAudio(song_list[id][2][0])
        return
    
    for i in range(n):
        if len(song_list[id][0]) > 0:
            song_list[id][0].pop(0)
            song_list[id][1].pop(0)
            song_list[id][2].pop(0)
    

@bot.command()
async def clear(ctx):
    id = ctx.guild.id
    check_queue(id, False, n=len(song_list[id][0]))
    
    text = "The queue has been cleared."
    embed=discord.Embed(description=text, color=0xff0000)
    await ctx.send(embed = embed)


@bot.command()
async def queue(ctx):

    if len(song_list[ctx.guild.id][1]) == 0: 
        text = "There is currently no song in the queue."
        color = 0xffb032
    else:
        text = array_to_string(song_list[ctx.guild.id][1])
        color = 0xff0000
    
    embed=discord.Embed(description=text, color=color)
    await ctx.send(embed = embed)


@bot.command()
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    
    id = ctx.guild.id
    check_queue(id, False, n=len(song_list[id][0]))


@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.pause()
    
    text = "Paused the song."
    embed=discord.Embed(description=text, color=0xff0000)
    await ctx.send(embed = embed)


@bot.command()
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.resume()
    
    text = "Resumed the song."
    embed=discord.Embed(description=text, color=0xff0000)
    await ctx.send(embed = embed)


@bot.command()
async def loop(ctx):

    if song_list[ctx.guild.id][3] == True:
        song_list[ctx.guild.id][3] = False
        text = "Looping disabled."
    else:
        song_list[ctx.guild.id][3] = True
        text = "Looping enabled."

    embed=discord.Embed(description=text, color=0xff0000)
    await ctx.send(embed = embed)


@bot.command()
async def skip(ctx, n=1):
    voice = get(bot.voice_clients, guild=ctx.guild)

    id = ctx.guild.id
    if n > 1: check_queue(id, False, n=n-1)
    voice.stop()


    queued = len(song_list[ctx.guild.id][1])
    
    if queued > 0: title = f"Now playing"
    else: return

    text = song_list[ctx.guild.id][1]
    text = f'{song_list[ctx.guild.id][1][1].split(" [")[0]}'
    embed=discord.Embed(title=title,description=text, color=0xff0000)
    await ctx.send(embed = embed)


@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    id = ctx.guild.id
    check_queue(id, False, n = len(song_list[id][0]))

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")





"""
$$\       $$$$$$\   $$$$$$\  $$$$$$$\   $$$$$$\  
$$ |     $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ 
$$ |     $$ /  $$ |$$ /  $$ |$$ |  $$ |$$ /  \__|
$$ |     $$ |  $$ |$$ |  $$ |$$$$$$$  |\$$$$$$\  
$$ |     $$ |  $$ |$$ |  $$ |$$  ____/  \____$$\ 
$$ |     $$ |  $$ |$$ |  $$ |$$ |      $$\   $$ |
$$$$$$$$\ $$$$$$  | $$$$$$  |$$ |      \$$$$$$  |
\________|\______/  \______/ \__|       \______/
"""

bot.loop.create_task(crypto_bot())
bot.loop.create_task(covid_bot())
bot.run(TOKEN)