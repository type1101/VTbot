import os
from dotenv import load_dotenv
import requests
import feedparser
from database import initdb    ######, is_article_new, save_article


initdb()

load_dotenv()

token = os.getenv('TOKEN_TELEGRAM')
chat_id = int(os.getenv('CHAT_ID_TELEGRAM'))

def send_message(to_send):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {
        'chat_id' : chat_id, 
        'text' : to_send
    }
    try : 
        requests.post(url= url, data= data, timeout=10)

    except Exception as e:
        print (f"erreur : {e}")



def check_react_news():

    feed = feedparser.parse("https://react.dev/rss.xml")

    ###### premier message ######

    title = feed.entries[0].title
    desc = feed.entries[0].description
    link = feed.entries[0].link

    message = f"📢 {title}\n\n{desc}\n\n🔗 {link}"
    send_message(message)


  

check_react_news()
