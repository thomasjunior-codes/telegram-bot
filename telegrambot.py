import requests
import os

headers = {
    "User-Agent": "TelegramWikiBot/1.0"
}

wiki_api = "https://ta.wikipedia.org/w/api.php"

# STEP 1 — Get random article
random_params = {
    "action": "query",
    "format": "json",
    "list": "random",
    "rnnamespace": 0,
    "rnlimit": 1
}

random_res = requests.get(wiki_api, params=random_params, headers=headers).json()
title = random_res["query"]["random"][0]["title"]

# STEP 2 — Get FULL article content
extract_params = {
    "action": "query",
    "format": "json",
    "prop": "extracts",
    "explaintext": True,
    "titles": title
}

extract_res = requests.get(wiki_api, params=extract_params, headers=headers).json()
page = next(iter(extract_res["query"]["pages"].values()))
extract = page.get("extract", "No content available.")

link = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

message = f"📚 {title}\n\n{extract}\n\n🔗 Read more: {link}"

bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']
send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

MAX_LENGTH = 4000

# Auto split for Telegram limit
for i in range(0, len(message), MAX_LENGTH):
    part = message[i:i+MAX_LENGTH]
    requests.post(send_url, data={
        "chat_id": chat_id,
        "text": part
    })
