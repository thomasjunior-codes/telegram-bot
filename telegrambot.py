import requests
import os

headers = {
    "User-Agent": "TelegramWikiBot/1.0"
}

# STEP 1: Get random article title first
random_api = "https://en.wikipedia.org/w/api.php"

params = {
    "action": "query",
    "format": "json",
    "list": "random",
    "rnnamespace": 0,
    "rnlimit": 1
}

random_res = requests.get(random_api, params=params, headers=headers).json()
title = random_res["query"]["random"][0]["title"]

# STEP 2: Get FULL extract (not just short summary)
extract_params = {
    "action": "query",
    "format": "json",
    "prop": "extracts",
    "explaintext": True,
    "titles": title
}

extract_res = requests.get(random_api, params=extract_params, headers=headers).json()

page = next(iter(extract_res["query"]["pages"].values()))
full_extract = page.get("extract", "No extract available.")

link = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

# STEP 3: Translate to Tamil
translate_url = "https://translate.googleapis.com/translate_a/single"

def translate_to_tamil(text):
    params = {
        "client": "gtx",
        "sl": "en",
        "tl": "ta",
        "dt": "t",
        "q": text
    }
    response = requests.get(translate_url, params=params).json()
    return response[0][0][0]

tamil_title = translate_to_tamil(title)
tamil_extract = translate_to_tamil(full_extract[:3000])  # limit length

# STEP 4: Send to Telegram
message = f"📚 {tamil_title}\n\n{tamil_extract}\n\n🔗 {link}"

bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']

send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

requests.post(send_url, data={
    "chat_id": chat_id,
    "text": message
})
