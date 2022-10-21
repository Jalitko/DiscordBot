import json
from lxml import html
import requests
import cbpro
from PIL import Image
import subprocess


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


from vars import *
"""
def prefix(bot, message):
    data = read()
    id = str(message.guild.id)

    try: prefix = data[id][0]["prefix"]
    except: prefix = default_prefix

    return prefix
    """
def prefix(bot, message):
    data = read()
    #print(str(message.guild))
    id = str(message.guild)

    try: prefix = data[id][0]["prefix"]
    except: prefix = default_prefix

    return prefix

def read():
    with open(json_file,"r") as p:
        data = json.load(p)
    return data


def write(data):
    with open(json_file, 'w') as p:
        json.dump(data, p)


def ismove(server_id):
    data = read()
    return data[str(server_id)][0]["move"]


def inroles(id,member):
    
    data = read()
    roles = data[str(id)][0]["roles"]

    for m in member:
        if str(m) in roles: return True
    
    return False



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



def write_data(path, what):
    last_num = open(path, "w")
    last_num.write(str(what))
    last_num.close()

def positive(path):
    page = requests.get('https://korona.gov.sk/koronavirus-na-slovensku-v-cislach/')
    tree = html.fromstring(page.content)
    positive = tree.xpath(path)

    positive = ''.join(positive)

    if  not positive.isdigit():
        positive = positive.replace('\xa0','')
    return positive




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



def format_int(a):
    return "{:,}".format(int(a)).replace(",", " ")

def format_float(a):
    if "e-" in str(a):  
        a = str(a)

        k = int(a[-1])
        z = substring(a, ".", "e")

        return format(float(a), f'.{k+len(z)}f')

    return "{:,}".format(float(a)).replace(",", " ")


def percentage_str(x, y):
    a =round(x[0][y]/x[1][y]*100-100,2)
    if a > 0: a = f"+{a}%"
    else: a = f"{a}%"
    return a

def percentage_float(x, y):
    a =round(x[0][y]/x[1][y]*100-100,2)
    return a


def substring(whole, sub1, sub2):
    return whole[whole.index(sub1)+1 : whole.index(sub2)]

def get_prices(coins_all):
    coins = [c["short"] for i,c in coins_all.items()]
    to = [c["to"] for i,c in coins_all.items()]
    
    public_client = cbpro.PublicClient()
    array_price = []
    array_24h = []

    for i,j in zip(coins, to):
        coin = f'{i}-{j}'

        price = public_client.get_product_ticker(coin)["price"]
        price = float(price)
        
        last_24h = public_client.get_product_24hr_stats(coin)["open"]
        last_24h = float(last_24h)
        
        array_price.append(price)
        array_24h.append(last_24h)
    
    return [array_price,array_24h]




def coins_chart(index):

    coin = coins[index]["name"]
    command = [
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', '--user-data-dir=D:\\Python\\Memory\\WebWhatsAppBot', 
        '--headless', 
        '--disable-gpu', 
        '--screenshot=C:\\vs\\dc\\corner\\chart.png', 
        '--window-size=2560,1440', 
        '--force-device-scale-factor=3', 
        f'https://coinmarketcap.com/sk/currencies/{coin}/'
    ]

    subprocess.run(command)

    im = Image.open(r"chart.png")
    
    width, height = im.size
    
    left = 1775
    top = 2095
    right = left + 2773
    bottom = top + 1230

    area = (left, top, right, bottom)
    im1 = im.crop(area)
    
    im1.save("chart.png")



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


import re
import urllib.request


def delete_symbols(title):
    symbols= ['.',',','*','?',':','/','"',">",'<','|', '#', "'"]
    for i in symbols:
            title = title.replace(i,'')
    return title


def title_to_url(title):
    title = title.replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + title)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v=" + video_ids[0]

def time_length(n):
    if n > 60**2:
        hour = n//60**2
        min  = n//60 - hour*60
        sec  = n - hour*(60**2) - min*60
        return f"{hour}:{min}:{sec}"
    else:
        min = n//60
        return f"{min}:{n-min*60}"

def array_to_string(x):
    str = ""
    n = "\n"
    for i,j in enumerate(x):
        if i+1 == len(x): n = ""
        str += f"**{i+1}.** {j}{n}"
    return str
