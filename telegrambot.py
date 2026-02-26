import requests
import os

url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

headers = {
    "User-Agent": "TelegramWikiBot/1.0 (https://github.com/thomasjunior-codes)"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Wikipedia API failed:", response.status_code)
    exit()

try:
    res = response.json()
except Exception as e:
    print("JSON decode failed")
    print(response.text)
    exit()

title = res.get("title", "No Title")
summary = res.get("extract", "No summary available.")
link = res.get("content_urls", {}).get("desktop", {}).get("page", "")

message = f"📚 {title}\n\n{summary}\n\nRead more: {link}"

bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']

send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

requests.post(send_url, data={
    "chat_id": chat_id,
    "text": message
})
