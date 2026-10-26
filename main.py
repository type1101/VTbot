import os
from dotenv import load_dotenv
import feedparser
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import initdb, is_article_new, save_article

load_dotenv()

token = os.getenv("TOKEN_TELEGRAM")
bot = telebot.TeleBot(token)

initdb()

FEEDS = {
    "react": {
        "name": "React",
        "url": "https://react.dev/rss.xml"
    },
    "python": {
        "name": "Python",
        "url": "https://python.developpez.com/index/rss"
    },
    "docker": {
        "name": "Docker",
        "url": "https://www.docker.com/feed/"
    }
}


def generate_menu():
    """Génère le clavier de sélection des technologies."""
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    buttons = [
        InlineKeyboardButton("⚛️ React", callback_data="react"),
        InlineKeyboardButton("🐍 Python", callback_data="python"),
        InlineKeyboardButton("🐳 Docker", callback_data="docker")
    ]
    markup.add(*buttons)
    return markup


def check_news(target_chat_id, feed_key):
    """Scanne le flux sélectionné et envoie les nouveaux articles."""
    feed_data = FEEDS[feed_key]
    feed = feedparser.parse(feed_data["url"])
    new_articles_count = 0

    bot.send_message(target_chat_id, f"🔍 Scan en cours pour {feed_data['name']}...")

    for entry in reversed(feed.entries):
        link = entry.link
        title = entry.title
        desc = getattr(entry, "description", "")
        if len(desc) > 350:
            desc = desc[:350] + "..."

        if is_article_new(link):
            message = f"📢 [{feed_data['name']}] {title}\n\n{desc}\n\n🔗 {link}"
            bot.send_message(target_chat_id, message)
            save_article(link, title, feed_data['name'])
            new_articles_count += 1
            print(f"[{feed_data['name']}] Article envoyé : {title}")

    if new_articles_count == 0:
        bot.send_message(target_chat_id, f"✅ Aucun nouvel article pour {feed_data['name']} pour le moment, voici les derniers news.")
        link = feed.entries[0].link
        title = feed.entries[0].title
        desc = feed.entries[0].description
        message = f"📢 [{feed_data['name']}] {title}\n\n{desc}\n\n🔗 {link}"
        bot.send_message(target_chat_id, message)
        print(f"[{feed_data['name']}] Dernier article envoyé : {title}")


@bot.message_handler(commands=["start", "menu", "hello", "coucou"])
def send_welcome(message):
    """Répond en affichant le clavier interactif."""
    bot.send_message(
        message.chat.id,
        "👋 Choisis une technologie pour consulter les dernières actus :",
        reply_markup=generate_menu()
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_menu_click(call):
    """Détecte le clic sur l'un des boutons du menu."""
    if call.data in FEEDS:
        # Informe Telegram que le clic a été reçu (retire l'animation de chargement du bouton)
        bot.answer_callback_query(call.id)
        check_news(call.message.chat.id, call.data)


if __name__ == "__main__":
    print("🤖 Bot démarré et à l'écoute des commandes...")
    bot.infinity_polling()