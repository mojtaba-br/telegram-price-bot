# main.py
import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.error import TelegramError
from apscheduler.schedulers.blocking import BlockingScheduler
import jdatetime
import pytz

# ================= CONFIG =================
TOKEN = os.getenv("BOT_TOKEN")  # دریافت امن توکن از Environment Variable
CHANNEL_ID = "-1003029415789"

URLS = {
    "dollar": "https://alanchand.com/currencies-price/usd",
    "gold": "https://alanchand.com/gold-price/18ayar",
    "full_coin": "https://alanchand.com/gold-price/bahar",
    "half_coin": "https://alanchand.com/gold-price/nim",
    "quarter_coin": "https://alanchand.com/gold-price/rob"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.1 Safari/537.36"
}

bot = Bot(token=TOKEN)
scheduler = BlockingScheduler()

# ================= FUNCTIONS =================
def fetch_price(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.find("span", class_="price")
        if price_tag:
            return price_tag.text.strip()
        else:
            return "خطا در دریافت قیمت"
    except Exception as e:
        print("Error fetching price:", e)
        return "خطا در دریافت قیمت"

def send_prices():
    try:
        # گرفتن زمان تهران به شمسی
        tz = pytz.timezone("Asia/Tehran")
        now = jdatetime.datetime.fromgregorian(datetime=jdatetime.datetime.now(tz))
        date_str = now.strftime("%A %d %B %Y")
        time_str = now.strftime("%H:%M")
        
        # گرفتن قیمت‌ها
        dollar = fetch_price(URLS["dollar"])
        gold = fetch_price(URLS["gold"])
        full_coin = fetch_price(URLS["full_coin"])
        half_coin = fetch_price(URLS["half_coin"])
        quarter_coin = fetch_price(URLS["quarter_coin"])
        
        message = f"""📈 آخرین قیمت‌های بازار
🕐 {date_str} - ساعت {time_str}

💵 دلار آمریکا: {dollar} تومان
🏅 طلای ۱۸ عیار: {gold} تومان
🥇 سکه تمام بهار آزادی: {full_coin} تومان
🥈 نیم سکه: {half_coin} تومان
🥉 ربع سکه: {quarter_coin} تومان

🔄 بروزرسانی هر دقیقه
@gheymat_tala_va_dolar_bot"""
        
        bot.send_message(chat_id=CHANNEL_ID, text=message)
        print("Prices sent successfully.")
        
    except TelegramError as e:
        print("Telegram error:", e)
    except Exception as e:
        print("General error:", e)

# ================= SCHEDULER =================
scheduler.add_job(send_prices, 'interval', minutes=1)

print("Bot started and scheduler running...")
send_prices()  # پیام اولی هم فرستاده میشه
scheduler.start()
