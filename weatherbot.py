import requests
import os

bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['TOURISM_CHAT_ID']

# top 50 tourist places
places = [
("Alagar Kovil",10.0407,78.2130),
("Avalanche Lake",11.3080,76.5880),
("Chennai Marina Beach",13.0500,80.2824),
("Chidambaram",11.3996,79.6936),
("Coonoor",11.3530,76.7950),
("Courtallam",8.9340,77.2770),
("Darasuram Temple",10.9480,79.3567),
("Dhanushkodi",9.1790,79.4214),
("Doddabetta Peak",11.4040,76.7350),
("Gangaikonda Cholapuram",11.2076,79.4444),
("Gingee Fort",12.2510,79.4170),
("Hogenakkal Falls",12.1180,77.7743),
("Kallanai Dam",10.8503,78.8867),
("Kanchipuram",12.8342,79.7036),
("Kanyakumari",8.0883,77.5385),
("Kodaikanal Lake",10.2381,77.4892),
("Kolli Hills",11.2480,78.3450),
("Kotagiri",11.4200,76.8600),
("Kumbakonam",10.9598,79.3845),
("Madurai",9.9195,78.1193),
("Mahabalipuram",12.6269,80.1920),
("Manjolai Hills",8.7030,77.3950),
("Meghamalai",9.6555,77.3996),
("Mudumalai Park",11.5586,76.5340),
("Nagapattinam Beach",10.7667,79.8431),
("Namakkal Fort",11.2194,78.1674),
("Nilgiri Railway",11.4100,76.6950),
("Ooty",11.4064,76.6932),
("Padmanabhapuram Palace",8.2503,77.3257),
("Palani",10.4503,77.5209),
("Pamban Bridge",9.2770,79.1994),
("Papanasam Falls",8.7084,77.3580),
("Pichavaram Mangrove",11.4293,79.7830),
("Pillar Rocks",10.2310,77.4870),
("Rameswaram",9.2881,79.3174),
("Silver Cascade Falls",10.2453,77.4960),
("Srirangam",10.8623,78.6900),
("Suruli Falls",9.6794,77.2730),
("Thanjavur Temple",10.7828,79.1314),
("Thirumalai Nayakkar Mahal",9.9252,78.1198),
("Thiruvalluvar Statue",8.0786,77.5500),
("Tiruchendur",8.4987,78.1194),
("Tiruvannamalai",12.2319,79.0677),
("Trichy Rockfort",10.8262,78.6932),
("Velankanni",10.6833,79.8500),
("Vellore Fort",12.9165,79.1325),
("Vivekananda Rock",8.0780,77.5500),
("Yanaimalai",10.0180,78.2130),
("Yelagiri Hills",12.5670,78.6390),
("Yercaud",11.7753,78.2090)
]

# Weather code mapping
weather_codes = {
0:"Clear sky ☀️",
1:"Mainly clear 🌤️",
2:"Partly cloudy ⛅",
3:"Overcast ☁️",
45:"Fog 🌫️",
48:"Depositing rime fog 🌫️",
51:"Light drizzle 🌦️",
53:"Moderate drizzle 🌦️",
55:"Dense drizzle 🌧️",
56:"Light freezing drizzle ❄️🌧️",
57:"Dense freezing drizzle ❄️🌧️",
61:"Slight rain 🌧️",
63:"Moderate rain 🌧️",
65:"Heavy rain 🌧️",
66:"Light freezing rain ❄️🌧️",
67:"Heavy freezing rain ❄️🌧️",
71:"Slight snow ❄️",
73:"Moderate snow ❄️",
75:"Heavy snow ❄️",
77:"Snow grains ❄️",
80:"Slight rain showers 🌦️",
81:"Moderate rain showers 🌦️",
82:"Violent rain showers ⛈️",
85:"Slight snow showers ❄️",
86:"Heavy snow showers ❄️",
95:"Thunderstorm ⛈️",
96:"Thunderstorm with hail ⛈️",
99:"Heavy hail thunderstorm ⛈️"
}

# Build single API request
latitudes = ",".join(str(p[1]) for p in places)
longitudes = ",".join(str(p[2]) for p in places)

url = f"https://api.open-meteo.com/v1/forecast?latitude={latitudes}&longitude={longitudes}&current_weather=true"

response = requests.get(url, timeout=30)
data = response.json()

weather_list = data

message = "🌤️ Tamil Nadu Tourist Weather\n\n"

for i, place in enumerate(places):
    name = place[0]
    temp = weather_list[i]["current_weather"]["temperature"]
    wind = weather_list[i]["current_weather"]["windspeed"]
    code = weather_list[i]["current_weather"]["weathercode"]
    condition = weather_codes.get(code,"Unknown")
    message += f"{name}: {temp}°C, 🌬️: {wind}km/h, {condition}\n"
    
# Send Telegram message
telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

requests.post(
    telegram_url,
    data={
        "chat_id": chat_id,
        "text": message
    },
    timeout=20
)
