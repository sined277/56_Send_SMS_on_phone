import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# OpenWeatherMap API endpoint and API key
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_KEY")

# Twilio account details (you need to replace with your own details)
account_sid = "YOUR ACCOUNT SID"
auth_token = os.environ.get("AUTH_TOKEN")

# Weather parameters (latitude, longitude, API key, and weather data to exclude)
weather_params = {
    "lat": "YOUR LATITUDE",
    "lon": "YOUR LONGITUDE",
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

# Get weather data from OpenWeatherMap API
response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()  # Raise an exception if the status code indicates an error
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]  # Get the next 12 hours of weather data

will_rain = False

# Check if it will rain in the next 12 hours
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:  # Condition code less than 700 means it will rain
        will_rain = True

# If it will rain, send a message using Twilio API
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_="YOUR TWILIO VIRTUAL NUMBER",
        to="YOUR TWILIO VERIFIED REAL NUMBER"
    )
    print(message.status)  # Print the status of the message (e.g. 'queued' or 'sent')
