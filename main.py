import os
import requests
import urllib.parse
import sys

# --- CONFIGURATION ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

VIDEO_DIR = "content/video"

def get_ai_caption(filename):
    topic = filename.replace(".mp4", "").replace("_", " ")
    # Physics specific prompt
    prompt = (
        f"Write a short, engaging Instagram caption for a physics video about '{topic}'. "
        "Include 3-4 interesting facts and SEO hashtags like #Physics #Science #Education. "
        "Keep it exciting for students."
    )
    
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
            data = {"reqtype": "fileupload", "userhash": ""}
            files = {"fileToUpload": f}
            response = requests.post(url, data=data, files=files)
            if response.status_code == 200:
                return response.text.strip()
            else:
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
    # 1. Folder check karein
    if not os.path.exists(VIDEO_DIR):
        print("Video directory not found.")
        return

    # 2. Available videos list karein
    files = [f for f in os.listdir(VIDEO_DIR) if f.endswith(('.mp4', '.mkv', '.mov'))]
    
    if not files:
        print("No videos left in the folder!")
        sys.exit(0) # Exit cleanly

    # 3. Sirf ek video select karein (Pehla wala)
    video_to_process = files[0]
    file_path = os.path.join(VIDEO_DIR, video_to_process)
    print(f"Processing video: {video_to_process}")

    # 4. Catbox Upload
    catbox_url = upload_to_catbox(file_path)
    if not catbox_url:
        print("Upload failed. Keeping file for next try.")
        sys.exit(1) # Error exit
    
    print(f"Uploaded: {catbox_url}")

    # 5. AI Caption
    caption = get_ai_caption(video_to_process)

    # 6. Send
    send_to_telegram(catbox_url, caption)
    send_to_webhook(catbox_url, caption)

    # 7. DELETE VIDEO (Main Logic)
    try:
        os.remove(file_path)
        print(f"SUCCESS: Deleted {video_to_process} from local storage.")
    except Exception as e:
        print(f"Error deleting file: {e}")

if __name__ == "__main__":
    main()
