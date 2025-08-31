import requests
from bs4 import BeautifulSoup
from telegram import Bot
import jdatetime
import pytz
import time
import os

# گرفتن توکن و کانال از Environment Variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)

# لینک‌ها
URLS = {
    "dollar": ("💵 دلار آمریکا", "https://alanchand.com/currencies-price/usd"),
    "gold18": ("🏅 طلای ۱۸ عیار", "https://alanchand.com/gold-price/18ayar"),
    "seke_tamam": ("🥇 سکه تمام بهار آزادی", "https://alanchand.com/gold-price/bahar"),
    "nim": ("🥈 نیم سکه", "https://alanchand.com/gold-price/nim"),
    "rob": ("🥉 ربع سکه", "https://alanchand.com/gold-price/rob"),
}

import requests
from bs4 import BeautifulSoup

def fetch_price(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.1 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # خطای HTTP رو بالا می‌اندازه اگر بود
        soup = BeautifulSoup(response.text, "html.parser")
        
        # پیدا کردن قیمت (فرض میکنیم span با کلاس price)
        price_tag = soup.find("span", class_="price")
        if price_tag:
            price = price_tag.text.strip()
            return price
        else:
            return "خطا در دریافت قیمت"
    except Exception as e:
        print("Error fetching price:", e)
        return "خطا در دریافت قیمت"


def make_message():
    # تاریخ و ساعت به وقت تهران
    tz = pytz.timezone("Asia/Tehran")
    now_tehran = jdatetime.datetime.now(tz)
    date_str = now_tehran.strftime("%A %d %B %Y - ساعت %H:%M")

    # قیمت‌ها
    prices = []
    for key, (label, url) in URLS.items():
        prices.append(f"{label}: {fetch_price(url)} تومان")

    message = (
        "📈 آخرین قیمت‌های بازار\n"
        f"🕐 {date_str}\n\n"
        + "\n".join(prices) +
        "\n\n🔄 بروزرسانی هر دقیقه\n"
        "@gheymat_tala_va_dolar_bot"
    )
    return message

def main():
    while True:
        try:
            msg = make_message()
            bot.send_message(chat_id=CHANNEL_ID, text=msg)
        except Exception as e:
            print("خطا:", e)
        time.sleep(60)  # هر ۱ دقیقه

if __name__ == "__main__":
    main()
