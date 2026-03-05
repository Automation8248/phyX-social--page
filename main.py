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
from webdriver_manager.chrome import ChromeDriverManager

# --- 1. SETUP FOLDERS (EXISTING) ---
os.makedirs("output_images", exist_ok=True)

# --- 2. 30+ UNIQUE TITLES & CAPTIONS (EXISTING) ---
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

# --- 3. HASHTAG CATEGORIES (EXISTING) ---
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

# --- 4. SECRETS (EXISTING) ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
WEBHOOK = os.getenv('WEBHOOK_URL')

def setup_browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
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
        # STEP 1: Website open karna aur wait karna
        print("🌐 Opening DeepAI Chat...")
        driver.get("https://deepai.org/chat")
        
        # DeepAI Chat ke specific input box ka wait karna
        # Selector ko visual reference 'image_2.png' ke basis par adjust kiya hai
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "chat-input-area")))
        time.sleep(3) 
        
        take_screenshot(driver, "1_website_opened")
        
        # STEP 2: Human Behavior Scroll
        human_like_scroll(driver)
        
        # STEP 3: Prompt type karna (IMPROVED HUMAN BEHAVIOR AS PER REQUEST)
        print("⌨️ Interaction with typing bar...")
        # DeepAI Chat has a unique input div structure.
        chat_box_container = driver.find_element(By.CLASS_NAME, "chat-input-area")
        
        # Pahle us typing bar par click karega like a human to focus
        print("🖱️ Clicking typing bar...")
        actions.move_to_element(chat_box_container).click().perform() 
        time.sleep(1) # Delay between click and typing to simulate human speed
        
        # Then जल्दी-जल्दी type karega
        print("⌨️ Typing prompt quickly...")
        # standard send_keys usually performs quick typing
        chat_box_container.send_keys(f"Generate an image: {prompt}")
        time.sleep(2) # Delay between typing and sending for review (human behavior)
        
        take_screenshot(driver, "2_prompt_typed_before_send")
        
        # STEP 4: Send button click karna (The Blue Circle from image_2.png)
        # Unique blue circular button ke liye selector. Previous selector ko general blue send button search karne ke liye refine kiya hai.
        print("🖱️ Clicking blue send button...")
        send_btn = driver.find_element(By.CLASS_NAME, "chat-send-button")
        
        # Explicit move and click for human simulation
        actions.move_to_element(send_btn).click().perform()
        
        print(f"⏳ Waiting for image generation... Prompt: {prompt}")
        time.sleep(35) # DeepAI processing time
        
        # STEP 5: Image generate hone ke baad wait karna (EXISTING)
        images = driver.find_elements(By.TAG_NAME, "img")
        latest_image = images[-1] # Usually the last image tag after generation
        print("✅ Image generated! Waiting 2 seconds as human behavior...")
        time.sleep(2)
        
        take_screenshot(driver, "3_image_generated")

        # STEP 6: Mouse se image par hover aur click karna (EXISTING HUMAN BEHAVIOR)
        print("🖱️ Moving mouse to image and clicking...")
        actions.move_to_element(latest_image).click().perform()
        time.sleep(1)
        
        # Image URL nikal kar download karna (EXISTING)
        img_url = latest_image.get_attribute("src")
        img_data = requests.get(img_url).content
        saved_img_path = f"output_images/final_generated_image.jpg"
        
        with open(saved_img_path, 'wb') as handler:
            handler.write(img_data)
        print(f"💾 Image successfully downloaded at {saved_img_path}")

        # STEP 7: POST TO TELEGRAM (Only Image + DateTime) (EXISTING)
        print("🚀 Sending to Telegram...")
        tg_text = f"📷 <b>New AI Anime Art</b>\n\n⏰ <b>Timestamp:</b> {dt_string}"
        with open(saved_img_path, 'rb') as photo:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': CHAT_ID, 'caption': tg_text, 'parse_mode': 'HTML'},
                          files={'photo': photo})

        # STEP 8: POST TO WEBHOOK (All Info + Hashtags) (EXISTING)
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
