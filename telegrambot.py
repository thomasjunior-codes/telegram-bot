import requests
import os

# Step 1: Get random Wikipedia article
wiki_url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

headers = {
    "User-Agent": "TelegramWikiBot/1.0 (https://github.com/thomasjunior-codes)"
}

response = requests.get(wiki_url, headers=headers)

if response.status_code != 200:
    print("Wikipedia API failed:", response.status_code)
    exit()

res = response.json()

title = res.get("title", "")
summary = res.get("extract", "")
link = res.get("content_urls", {}).get("desktop", {}).get("page", "")

# Step 2: Translate to Tamil (FREE trick)
translate_url = "https://translate.googleapis.com/translate_a/single"

params = {
    "client": "gtx",
    "sl": "en",
    "tl": "ta",
    "dt": "t",
    "q": summary
}

translation = requests.get(translate_url, params=params).json()
tamil_summary = translation[0][0][0]

# Optional: Translate title
params["q"] = title
title_translation = requests.get(translate_url, params=params).json()
tamil_title = title_translation[0][0][0]

# Step 3: Send to Telegram
message = f"📚 {tamil_title}\n\n{tamil_summary}\n\n🔗 {link}"

bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']

send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

requests.post(send_url, data={
    "chat_id": chat_id,
    "text": message
})
