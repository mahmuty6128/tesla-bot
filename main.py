import cloudscraper
from bs4 import BeautifulSoup
from telegram import Bot
import time
import os

TESLA_URL = "https://www.tesla.com/tr_tr/inventory/new/my"
TELEGRAM_TOKEN = os.getenv("7301767998:AAEDf3ymTnoXE8cCTg67VUpDTyBNFKZ25gE")
CHAT_ID = os.getenv("1251199930")

bot = Bot(token=TELEGRAM_TOKEN)

def check_inventory():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    scraper = cloudscraper.create_scraper()
    response = scraper.get(TESLA_URL, headers=headers, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    cars = soup.find_all("div", class_="result-container")
    found = []

    for car in cars:
        title = car.find("h2").text.strip() if car.find("h2") else "Model Bulunamadı"
        link_tag = car.find("a", href=True)
        link = "https://www.tesla.com" + link_tag['href'] if link_tag else "Bağlantı yok"
        found.append((title, link))

    return found

def main():
    print("🚀 Tesla bot başlatıldı...")
    bot.send_message(chat_id=CHAT_ID, text="✅ Tesla bot Render'da çalışıyor!")
    last_seen = set()

    while True:
        try:
            current = set(check_inventory())
            new = current - last_seen
            if new:
                for title, link in new:
                    bot.send_message(chat_id=CHAT_ID, text=f"🚗 Yeni Tesla bulundu: {title}\n🔗 {link}")
                last_seen = current
            else:
                print("Yeni araç yok.")
            time.sleep(300)  # 5 dakika
        except Exception as e:
            print("⚠️ Hata:", e)
            time.sleep(60)

if __name__ == "__main__":
    main()
