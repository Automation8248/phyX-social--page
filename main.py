import os
import requests
import urllib.parse
import sys

# --- CONFIGURATION ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

VIDEO_DIR = "content/video"

def get_formatted_caption(filename):
    """
    Generates a specific format:
    Hook
    .
    .
    .
    .
    .
    Hashtags
    """
    topic = filename.replace(".mp4", "").replace("_", " ")
    
    # Prompt logic: Hum AI ko bolenge Hook aur Hashtags ke beech mein '|' lagaye
    # Taki hum Python se usko todkar beech mein dots daal sakein perfect format ke liye.
    prompt = (
        f"Write a viral one-line hook sentence for a physics video about '{topic}'. "
        "Then write the symbol '|'. "
        "Then list 7 high-traffic SEO hashtags including #explore and #physics. "
        "Do not write anything else."
    )
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://text.pollinations.ai/{encoded_prompt}"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            content = response.text.strip()
            
            # Agar AI ne sahi se '|' lagaya hai to split karke format banayenge
            if "|" in content:
                parts = content.split("|")
                hook = parts[0].strip()
                hashtags = parts[1].strip()
            else:
                # Fallback agar AI format bhool gaya
                hook = content
                hashtags = f"#explore #physics #science #viral #{topic.replace(' ', '')}"
            
            # FINAL FORMATTING (Ye wahi structure hai jo aapne manga)
            final_caption = f"{hook}\n.\n.\n.\n.\n.\n{hashtags}"
            return final_caption
            
        else:
            return f"Physics Magic: {topic} ✨\n.\n.\n.\n.\n.\n#explore #physics #science"
            
    except Exception as e:
        print(f"AI Error: {e}")
        return f"Amazing Physics Fact: {topic}\n.\n.\n.\n.\n.\n#explore #physics #science"

def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    try:
        with open(file_path, "rb") as f:
            data = {"reqtype": "fileupload", "userhash": ""}
            files = {"fileToUpload": f}
            print("Uploading to Catbox (Max 60s)...")
            response = requests.post(url, data=data, files=files, timeout=60)
            if response.status_code == 200:
                return response.text.strip()
            else:
                return None
    except Exception as e:
        print(f"Upload Error: {e}")
        return None

def send_to_telegram(video_url, caption):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "video": video_url,
        "caption": caption,
    }
    # Timeout 10s
    requests.post(api_url, json=payload, timeout=10)

def send_to_webhook(video_url, caption):
    if not WEBHOOK_URL: 
        return

    # User requirement: "Content ke niche only caption aana chahie"
    # Isliye hum payload mein direct wahi caption bhej rahe hain
    payload = {
        "content": caption, 
        "video_url": video_url
    }
    requests.post(WEBHOOK_URL, json=payload, timeout=10)

def main():
    # 1. Folder Check
    if not os.path.exists(VIDEO_DIR):
        sys.exit(0)

    # 2. Files List
    files = [f for f in os.listdir(VIDEO_DIR) if f.endswith(('.mp4', '.mkv', '.mov'))]
    if not files:
        print("No videos found.")
        sys.exit(0)

    # 3. Process First Video
    video_to_process = files[0]
    file_path = os.path.join(VIDEO_DIR, video_to_process)
    print(f"Processing: {video_to_process}")

    # 4. Upload
    catbox_url = upload_to_catbox(file_path)
    if not catbox_url:
        print("Upload failed.")
        sys.exit(1)

    # 5. Generate Formatted Caption
    caption = get_formatted_caption(video_to_process)
    print("Caption Generated.")

    # 6. Send
    send_to_telegram(catbox_url, caption)
    send_to_webhook(catbox_url, caption)

    # 7. Delete File (Taaki repeat na ho)
    try:
        os.remove(file_path)
        print(f"Deleted: {video_to_process}")
    except Exception as e:
        print(f"Delete Error: {e}")

if __name__ == "__main__":
    main()
