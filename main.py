import os
import time
import random
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- 30+ UNIQUE TITLES ---
TITLES = [
    "Celestial Warrior Spirit", "Neon Tokyo Nights", "Sakura Petals Fall", "Cybernetic Samurai", 
    "Mystic Isekai Journey", "Midnight Ramen Vibes", "Golden Hour Shinobi", "Electric Dreamscape",
    "Azure Dragon Legacy", "Lost in Akihabara", "Shonen Power Surge", "Silent Ninja Shadow",
    "Ghibli Inspired Peace", "Mecha Strike Force", "Spirit of the Kitsune", "Vibrant Manga World",
    "Eternal Anime Sunset", "Crystal Clear Fantasy", "Retro Anime Aesthetic", "Supernatural Aura",
    "Urban Legend Hero", "Starlight Sorceress", "Infinity Blade Master", "Zen Garden Serenity",
    "Glitch Art Protagonist", "Crimson Battle Cry", "Oceanic Pearl Princess", "Techno Wizardry",
    "Parallel Universe Gate", "Legend of the Seven Stars", "Phantom Thief Mask", "Wind Walker"
]

# --- 30+ UNIQUE CAPTIONS ---
CAPTIONS = [
    "Witness the power of digital anime art! 🎨", "Every pixel tells a legendary story. ✨", 
    "Step into a world where imagination meets AI. 🌟", "The detail in this anime style is insane! 🔥",
    "Bringing your favorite tropes to life with AI. 📺", "Anime vibes to brighten your day. 🌈",
    "Exploring new dimensions of character design. 🤖", "A masterpiece born from a single prompt. ✍️",
    "Perfect wallpaper material, don't you think? 📱", "The future of anime art is here. 🚀",
    "Capturing the essence of classic shonen. ⚔️", "Soft aesthetic for a peaceful mood. ☁️",
    "Can you feel the intensity of this scene? ⚡", "Isekai dreams in high definition. 🌌",
    "Redefining the boundaries of AI creativity. 💡", "A tribute to the greats of manga history. 📚",
    "Neon lights and anime nights. 🌃", "Spirit and steel combined in one frame. 🎭",
    "Nature meets anime in this beautiful render. 🌿", "The ultimate fusion of art and technology. ⚙️",
    "Dark, mysterious, and absolutely epic. 🌑", "Vibrant colors for a vibrant soul. 🎨",
    "A journey through the lens of an AI artist. 📸", "Unleashing the hidden power within. 💎",
    "Simplicity is the ultimate sophistication. 🎐", "Ready for the next big adventure? 🗺️",
    "Where dreams and reality collide. 🌠", "An explosion of creativity and color. 💥",
    "Minimalist style with maximalist impact. 🖼️", "The art of the future, generated today. ⏳",
    "Join the otaku revolution! 🤜🤛", "Beyond the limits of human imagination. 🚀"
]

# --- HASHTAG CATEGORIES ---
FIXED_TAGS = "#Anime #AIArt #DeepAI #DigitalArt #OtakuCulture"
YT_TAGS = "#Shorts #AnimeEdits #YouTubeAnime #TrendingAnime #ViralArt"
FB_TAGS = "#AnimeCommunity #FacebookArt #OtakuWorld #AnimeFans #ArtSharing"
INSTA_TAGS = "#InstaAnime #AnimeGram #ArtOfToday #AnimeLovers #ExplorePage"

ANIME_PROMPTS = [
    "High quality anime girl with katana, cinematic lighting, 8k",
    "Cyberpunk city background anime style, neon colors",
    "Studio Ghibli forest landscape, detailed trees and water",
    "Epic anime battle scene with magic effects, vibrant colors"
]

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
WEBHOOK = os.getenv('WEBHOOK_URL')

def setup_browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def run_automation():
    driver = setup_browser()
    wait = WebDriverWait(driver, 40)
    
    # Random selection
    title = random.choice(TITLES)
    caption = random.choice(CAPTIONS)
    prompt = random.choice(ANIME_PROMPTS)
    
    # Detailed Date-Time
    now = datetime.now()
    dt_string = now.strftime("%A, %d %B %Y | %I:%M:%S %p")

    try:
        driver.get("https://deepai.org/chat")
        
        # Chat box input
        chat_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "chat-input-area")))
        chat_box.send_keys(f"Generate an image: {prompt}")
        
        # Send
        send_btn = driver.find_element(By.CLASS_NAME, "chat-send-button")
        send_btn.click()
        
        print(f"Generating for prompt: {prompt}...")
        time.sleep(30) # Waiting for image
        
        # Get Image URL
        images = driver.find_elements(By.TAG_NAME, "img")
        img_url = images[-1].get_attribute("src")

        # 1. TELEGRAM: Only Image + Date/Time
        tg_text = f"📷 <b>New AI Anime Art</b>\n\n⏰ <b>Timestamp:</b> {dt_string}"
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                      data={'chat_id': CHAT_ID, 'photo': img_url, 'caption': tg_text, 'parse_mode': 'HTML'})

        # 2. WEBHOOK: All details + Separate Hashtags
        webhook_payload = {
            "date_info": dt_string,
            "title": title,
            "caption": caption,
            "image_url": img_url,
            "hashtags": {
                "fixed": FIXED_TAGS,
                "youtube": YT_TAGS,
                "facebook": FB_TAGS,
                "instagram": INSTA_TAGS
            }
        }
        requests.post(WEBHOOK, json=webhook_payload)
        
        print(f"Successfully posted at {dt_string}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_automation()
