from dotenv import load_dotenv
import os
load_dotenv()

default_prefix = '?'
TOKEN = os.getenv('token')
json_file = "settigns.json"
song = "test.mp3"
default_activity = "?move Cukyna"
timeout_activity = "with Cukyna"


#COVID
last_date_txt = "covid/last_date.txt"
last_num_txt = "covid/last_num.txt"
hospitalized_txt = "covid/hospitalized.txt"
covid_chnnel = 890300334952546364



#emotes
emote_covid = "<:covid:893219430656532510>"
emote_Pepehands = "<:Pepehands:780141021199204392>"
emote_cryptotitle = ["<:FeelsHangMan:854009297222762527>", "<:PepeOk:780140991830687775>"]


#crypto
last_date_crpyto = "crypto/last_date.txt"
coins = {
    0: {'name': 'bitcoin',  'short': 'BTC',  "to": "EUR",  "toshort": "€", 'emote': '<:btc:893223507641655346>',  "color": 0xf2a900},
    1: {'name': 'ethereum', 'short': 'ETH',  "to": "EUR",  "toshort": "€", 'emote': '<:eth:893223522262999100>',  "color": 0xeceff0},
    2: {'name': 'dogecoin', 'short': 'DOGE', "to": "EUR",  "toshort": "€", 'emote': '<:doge:893223534959161387>', "color": 0xba9f33},
    3: {'name': 'shiba-inu','short': 'SHIB', "to": "EUR",  "toshort": "€", 'emote': '<:shib:901110543165820948>', "color": 0xf3a733},
    4: {'name': 'cosmos',   'short': 'ATOM', "to": "EUR",  "toshort": "€", 'emote': '<:atom:913792592091709440>', "color": 0x2E3148},
}

crypto_channel = 893185256490942484