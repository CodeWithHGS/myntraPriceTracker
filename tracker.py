from flask import Flask
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# ===== CONFIG =====
URL = "PASTE_YOUR_MYNTRA_PRODUCT_LINK"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# ===== TELEGRAM FUNCTION =====
def send(msg):
    r = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": msg
        },
        timeout=10
    )
    print("Telegram response:", r.text)


# ===== HOME ROUTE =====
@app.route("/", methods=["GET","HEAD"])
def home():
    return "Tracker running", 200


# ===== PRICE CHECK ROUTE =====
@app.route("/check", methods=["GET","HEAD"])
def check_price():

    print("Price checked")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
    }

    try:
        r = requests.get(URL, headers=headers, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        price_tag = soup.find("span", {"class": "pdp-price"})

        if price_tag:
            price = price_tag.text.strip()
            print("Price found:", price)

            send(f"Myntra price check:\n{price}")

        else:
            print("Price not found")

    except Exception as e:
        print("Error:", e)

    return "Checked", 200