import requests
import os
import random

headers = {
    "User-Agent": "TelegramWikiBot/1.0"
}

wiki_api = "https://en.wikipedia.org/w/api.php"

categories = [
    "Category:Science",
    "Category:History",
    "Category:Physics",
    "Category:Chemistry",
    "Category:Biology",
    "Category:World_history",
    "Category:Ancient_history",
    "Category:History_of_science"
]

bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']
send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

MAX_LENGTH = 4000

def send_message(text):
    for i in range(0, len(text), MAX_LENGTH):
        part = text[i:i+MAX_LENGTH]
        requests.post(send_url, data={
            "chat_id": chat_id,
            "text": part
        })

# Try multiple times to find long article
for attempt in range(5):

    chosen_category = random.choice(categories)

    category_params = {
        "action": "query",
        "format": "json",
        "generator": "categorymembers",
        "gcmtitle": chosen_category,
        "gcmnamespace": 0,
        "gcmlimit": 50,
        "prop": "extracts",
        "explaintext": True
    }

    response = requests.get(wiki_api, params=category_params, headers=headers).json()
    pages = response.get("query", {}).get("pages", {})

    if not pages:
        continue

    page = random.choice(list(pages.values()))
    title = page.get("title", "")
    extract = page.get("extract", "")

    if len(extract) > 2000:
        link = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
        message = f"📚 {title}\n\n{extract}\n\n🔗 Read more: {link}"
        send_message(message)
        break
else:
    # If no long article found after 5 attempts
    send_message("No suitable long science/history article found today. Try again tomorrow!")
