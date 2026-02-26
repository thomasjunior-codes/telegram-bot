import requests
import os
import random

headers = {
    "User-Agent": "TelegramWikiBot/1.0"
}

wiki_api = "https://en.wikipedia.org/w/api.php"

# STEP 1 — Choose random category
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

chosen_category = random.choice(categories)

# STEP 2 — Get random page from chosen category
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
    print("No pages found in category")
    exit()

page = random.choice(list(pages.values()))

title = page.get("title", "No title")
extract = page.get("extract", "")

# Skip short articles
if len(extract) < 1500:
    print("Article too short, skipping.")
    exit()

link = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

message = f"📚 {title}\n\n{extract}\n\n🔗 Read more: {link}"

bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']
send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

MAX_LENGTH = 4000

# Split message if long
for i in range(0, len(message), MAX_LENGTH):
    part = message[i:i+MAX_LENGTH]
    requests.post(send_url, data={
        "chat_id": chat_id,
        "text": part
    })
