import requests
from bs4 import BeautifulSoup
import os

URL = "PASTE_MYNTRA_PRODUCT_LINK"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

last_price = None

def send(msg):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg}
    )

r = requests.get(URL)
soup = BeautifulSoup(r.text, "html.parser")

price_tag = soup.find("span", {"class": "pdp-price"})

if price_tag:
    price = int(price_tag.text.replace("₹", "").replace(",", ""))

    if last_price is None:
        last_price = price

    if price < last_price:
        send(f"Price dropped! Now ₹{price}")

    last_price = price

print("Price checked")