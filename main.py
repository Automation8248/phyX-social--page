import os
import requests
import random
import urllib.parse

# --- CONFIGURATION ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

VIDEO_DIR = "content/video"
HISTORY_FILE = "history.txt"

def get_ai_caption(filename):
    # Filename se "_" hata kar topic banate hain
    topic = filename.replace(".mp4", "").replace("_", " ")
    
    prompt = (
        f"Write a short, engaging Instagram caption for a physics video about '{topic}'. "
        "Include 3-4 interesting facts and SEO hashtags like #Physics #Science #Education. "
        "Keep it exciting for students."
    )
    
    # Pollinations AI (Text API)
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://text.pollinations.ai/{encoded_prompt}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"Check out this amazing Physics video on {topic}! 🚀 #Physics #Science"
    except Exception as e:
        print(f"AI Error: {e}")
        return f"Amazing Physics content: {topic} #Science"

def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    try:
        with open(file_path, "rb") as f:
            data = {
                "reqtype": "fileupload",
                "userhash": "" # Optional
            }
            files = {"fileToUpload": f}
            response = requests.post(url, data=data, files=files)
            if response.status_code == 200:
                return response.text.strip() # Returns the URL
            else:
                print(f"Catbox Upload Failed: {response.text}")
                return None
    except Exception as e:
        print(f"Upload Error: {e}")
        return None

def send_to_telegram(video_url, caption):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "video": video_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    requests.post(api_url, json=payload)

def send_to_webhook(video_url, caption):
    if not WEBHOOK_URL: return
    payload = {
        "content": "New Physics Video Uploaded!",
        "video_url": video_url,
        "caption": caption
    }
    requests.post(WEBHOOK_URL, json=payload)

def main():
    # 1. Check History
    if not os.path.exists(HISTORY_FILE):
        open(HISTORY_FILE, 'w').close()
    
    with open(HISTORY_FILE, 'r') as f:
        used_videos = f.read().splitlines()

    # 2. Get Available Videos
    all_files = [f for f in os.listdir(VIDEO_DIR) if f.endswith(('.mp4', '.mkv', '.mov'))]
    available_videos = [f for f in all_files if f not in used_videos]

    if not available_videos:
        print("No new videos available to post.")
        exit()

    # 3. Select ONE video (First available)
    video_to_process = available_videos[0]
    file_path = os.path.join(VIDEO_DIR, video_to_process)
    print(f"Processing: {video_to_process}")

    # 4. Upload to Catbox
    catbox_url = upload_to_catbox(file_path)
    if not catbox_url:
        print("Failed to upload video.")
        exit(1)
    
    print(f"Uploaded to: {catbox_url}")

    # 5. Generate AI Caption
    caption = get_ai_caption(video_to_process)
    print(f"Generated Caption: {caption}")

    # 6. Send to Platforms
    send_to_telegram(catbox_url, caption)
    send_to_webhook(catbox_url, caption)

    # 7. Update History (Important logic to prevent repeats)
    with open(HISTORY_FILE, 'a') as f:
        f.write(video_to_process + "\n")
    print("History updated.")

if __name__ == "__main__":
    main()
