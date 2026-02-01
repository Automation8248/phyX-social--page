import os
import requests
import urllib.parse
import sys

# --- CONFIGURATION (Environment Variables) ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

VIDEO_DIR = "content/video"

def get_ai_caption(filename):
    """Generates a one-line Physics caption using Pollinations AI"""
    topic = filename.replace(".mp4", "").replace("_", " ")
    
    # YAHAN CHANGES KIYE HAIN:
    # "Exactly ONE sentence" aur "SEO hashtags" ka instruction diya hai
    prompt = (
        f"Write exactly ONE catchy sentence about '{topic}' for a physics video. "
        "Add 3-4 high-traffic SEO hashtags at the end. "
        "Do not write anything else."
    )
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://text.pollinations.ai/{encoded_prompt}"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.text
        else:
            # Fallback agar AI fail ho jaye
            return f"Watch this amazing physics concept: {topic} ⚛️ #Physics #Science #Education"
    except Exception as e:
        print(f"AI Error: {e}")
        return f"New Physics Video: {topic} #Physics #Science"

def upload_to_catbox(file_path):
    """Uploads video to Catbox.moe and returns the URL"""
    url = "https://catbox.moe/user/api.php"
    try:
        with open(file_path, "rb") as f:
            data = {"reqtype": "fileupload", "userhash": ""}
            files = {"fileToUpload": f}
            print("Uploading to Catbox (Max 60s)...")
            # Timeout 60s (Agar 1 min me upload nahi hua to fail)
            response = requests.post(url, data=data, files=files, timeout=60)
            if response.status_code == 200:
                return response.text.strip()
            else:
                print(f"Catbox Error: {response.text}")
                return None
    except Exception as e:
        print(f"Upload Exception: {e}")
        return None

def send_to_telegram(video_url, caption):
    """Sends the video URL and caption to Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing.")
        return

    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "video": video_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(api_url, json=payload, timeout=15)
        print("Sent to Telegram.")
    except Exception as e:
        print(f"Telegram Error: {e}")

def send_to_webhook(video_url, caption):
    """Sends the data to your Webhook"""
    if not WEBHOOK_URL: 
        return

    payload = {
        "content": "New Physics Video Dropped! ⚛️",
        "video_url": video_url,
        "caption": caption
    }
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print("Sent to Webhook.")
    except Exception as e:
        print(f"Webhook Error: {e}")

def main():
    print("--- Starting Physics Bot ---")

    # 1. Folder aur Files Check
    if not os.path.exists(VIDEO_DIR):
        print(f"Error: Directory '{VIDEO_DIR}' not found.")
        sys.exit(0)

    # Sirf .mp4 files dhoondhein
    files = [f for f in os.listdir(VIDEO_DIR) if f.endswith(('.mp4', '.mkv', '.mov'))]
    
    if not files:
        print("No videos found to process.")
        sys.exit(0) # Clean exit if empty

    # 2. Select First Video
    video_to_process = files[0]
    file_path = os.path.join(VIDEO_DIR, video_to_process)
    print(f"Selected Video: {video_to_process}")

    # 3. Upload (Critical Step)
    catbox_url = upload_to_catbox(file_path)
    if not catbox_url:
        print("Upload failed. Exiting WITHOUT deleting file.")
        sys.exit(1) # Error code taaki GitHub Actions fail mark ho
    
    print(f"Video URL: {catbox_url}")

    # 4. Generate AI Caption
    caption = get_ai_caption(video_to_process)
    print("Caption Generated.")

    # 5. Send to Platforms
    send_to_telegram(catbox_url, caption)
    send_to_webhook(catbox_url, caption)

    # 6. DELETE LOGIC (Process complete, delete local file)
    try:
        os.remove(file_path)
        print(f"SUCCESS: Deleted '{video_to_process}' to prevent repeat.")
    except Exception as e:
        print(f"Error deleting file: {e}")
        # Note: Agar yahan delete fail bhi hua, to GitHub Actions ka `git commit` step handle nahi karega.
        # Lekin `os.remove` usually reliable hota hai.

if __name__ == "__main__":
    main()
