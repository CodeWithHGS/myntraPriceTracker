import requests
from bs4 import BeautifulSoup
import time
import os

URL = "MYNTRA_PRODUCT_LINK"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

last_price = None

def send(msg):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg}
    )

while True:

    r = requests.get(URL)
    soup = BeautifulSoup(r.text,"html.parser")

    price = soup.find("span", {"class":"pdp-price"}).text
    price = int(price.replace("₹","").replace(",",""))

    global last_price

    if last_price is None:
        last_price = price

    if price < last_price:
        send(f"Price dropped! Now ₹{price}")

    last_price = price

    time.sleep(600)