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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# --- 1. SETUP FOLDERS ---
os.makedirs("output_images", exist_ok=True)

# --- 2. 60+ USER AGENTS ---
USER_AGENTS = [
    # Windows Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    # Windows Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    # Windows Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
    # Mac Chrome
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    # Mac Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    # Mac Firefox
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.3; rv:123.0) Gecko/20100101 Firefox/123.0",
    # Linux Chrome
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    # Linux Firefox
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    # Android Chrome
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; OnePlus 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; POCO F4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    # iOS Safari
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_7_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    # iOS Chrome
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/122.0.6261.62 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/121.0.6167.138 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/122.0.6261.62 Mobile/15E148 Safari/604.1",
    # Tablets & Misc
    "Mozilla/5.0 (Linux; Android 13; SM-X900) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Lenovo Tab P11 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS aarch64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

# --- 3. 30+ UNIQUE TITLES & CAPTIONS ---
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

# --- 4. HASHTAG CATEGORIES ---
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

# --- 5. SECRETS ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
WEBHOOK = os.getenv('WEBHOOK_URL')

def setup_browser():
    options = Options()
    random_ua = random.choice(USER_AGENTS)
    print(f"🕵️ Using Random User-Agent: {random_ua}")
    options.add_argument(f"user-agent={random_ua}")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def take_screenshot(driver, step_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"output_images/{step_name}_{timestamp}.png"
    driver.save_screenshot(filepath)
    print(f"📸 Screenshot saved: {filepath}")

def human_like_scroll(driver):
    print("🚶‍♂️ Simulating human scroll behavior...")
    for i in range(1, 600, 100):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.2)
    time.sleep(1)
    for i in range(600, 0, -150):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.2)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

def find_element_with_fallback(driver, wait, selectors, element_name):
    for by_type, selector_val in selectors:
        try:
            element = wait.until(EC.element_to_be_clickable((by_type, selector_val)))
            print(f"✅ Found {element_name} using: {selector_val}")
            return element
        except:
            continue
    return None

def run_automation():
    driver = setup_browser()
    wait = WebDriverWait(driver, 40)
    actions = ActionChains(driver)
    
    title = random.choice(TITLES)
    caption = random.choice(CAPTIONS)
    prompt = random.choice(ANIME_PROMPTS)
    
    now = datetime.now()
    dt_string = now.strftime("%A, %d %B %Y | %I:%M:%S %p")

    try:
        # STEP 1: Website open
        print("🌐 Opening DeepAI Chat...")
        driver.get("https://deepai.org/chat")
        time.sleep(5) 
        take_screenshot(driver, "1_website_opened")
        
        # STEP 2: Human Behavior Scroll
        human_like_scroll(driver)
        
        # STEP 3: FIND TYPING BAR WITH FALLBACKS
        print("🔍 Searching for typing bar...")
        chat_box_selectors = [
            (By.XPATH, "//textarea[contains(@placeholder, 'Message')]"), 
            (By.XPATH, "//input[contains(@placeholder, 'Message')]"), 
            (By.CSS_SELECTOR, "textarea[placeholder*='Message']"), 
            (By.TAG_NAME, "textarea"), 
            (By.CLASS_NAME, "chat-input-area") 
        ]
        
        chat_box_container = find_element_with_fallback(driver, wait, chat_box_selectors, "Typing Bar")
        
        if not chat_box_container:
            raise Exception("Typing bar screen par nahi mila. Selector update karna padega.")

        # Interaction - Click and Type
        print("🖱️ Clicking typing bar...")
        actions.move_to_element(chat_box_container).click().perform() 
        time.sleep(1)
        
        print("⌨️ Typing prompt quickly...")
        chat_box_container.send_keys(f"Generate an image: {prompt}")
        time.sleep(1.5) 
        take_screenshot(driver, "2_prompt_typed_before_enter")
        
        # STEP 4: SEND THE PROMPT USING KEYBOARD 'ENTER' (STRICT ORDER APPLIED)
        print("⌨️ Pressing 'ENTER' key on keyboard to send...")
        chat_box_container.send_keys(Keys.RETURN) # Ye Keyboard ka Enter button dabayega
        
        # Blue button logic ko sirf fallback ke taur par rakha hai, use nahi kiya jayega agar Enter se kaam ho gaya
        # Isliye purana code delete nahi kiya.
        
        print(f"⏳ Waiting for image generation... Prompt: {prompt}")
        time.sleep(35) 
        
        # STEP 5: Wait for generated image
        images = driver.find_elements(By.TAG_NAME, "img")
        latest_image = images[-1] 
        print("✅ Image generated! Waiting 2 seconds as human behavior...")
        time.sleep(2)
        take_screenshot(driver, "3_image_generated")

        # STEP 6: Hover and click image to download
        print("🖱️ Moving mouse to image and clicking...")
        actions.move_to_element(latest_image).click().perform()
        time.sleep(1)
        
        img_url = latest_image.get_attribute("src")
        img_data = requests.get(img_url).content
        saved_img_path = f"output_images/final_generated_image.jpg"
        
        with open(saved_img_path, 'wb') as handler:
            handler.write(img_data)
        print(f"💾 Image successfully downloaded at {saved_img_path}")

        # STEP 7: POST TO TELEGRAM
        print("🚀 Sending to Telegram...")
        tg_text = f"📷 <b>New AI Anime Art</b>\n\n⏰ <b>Timestamp:</b> {dt_string}"
        with open(saved_img_path, 'rb') as photo:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID, 'caption': tg_text, 'parse_mode': 'HTML'},
                          files={'photo': photo})

        # STEP 8: POST TO WEBHOOK
        print("🚀 Sending to Webhook...")
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
        
        print(f"🎉 All tasks completed successfully at {dt_string}!")

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        take_screenshot(driver, "error_state") 
    finally:
        driver.quit()

if __name__ == "__main__":
    run_automation()
