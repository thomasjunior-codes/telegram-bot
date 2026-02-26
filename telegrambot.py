import requests
import os

# Get random Wikipedia article
url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
res = requests.get(url).json()

title = res['title']
summary = res['extract']
link = res['content_urls']['desktop']['page']

message = f"📚 {title}\n\n{summary}\n\nRead more: {link}"

bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']

send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

requests.post(send_url, data={
    "chat_id": chat_id,
    "text": message
})
