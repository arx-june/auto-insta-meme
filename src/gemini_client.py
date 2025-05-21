# src/gemini_client.py

import time
import google.generativeai as genai
from config import GEMINI_API, DEBUG_MODE

# Configure the API key once
genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

def load_into_gemini(image_path: str, topic: str):
    """
    Uploads a file to Gemini, retrying on failure.
    Returns the upload reference on success, or None on permanent failure.
    """
    max_attempts = 3
    backoff = 2  # seconds

    for attempt in range(1, max_attempts + 1):
        try:
            if DEBUG_MODE:
                print(f"[DEBUG] Gemini upload attempt {attempt} for {image_path}")
            upload = genai.upload_file(
                path=image_path,
                mime_type="image/png",           # adjust if non-png
            )
            if DEBUG_MODE:
                print(f"[DEBUG] Gemini upload succeeded: {upload.name}")
            return upload
        except Exception as e:
            # Catch everything (including WinError 10060, httplib2 timeouts, etc.)
            if DEBUG_MODE:
                print(f"[DEBUG] Gemini upload failed (attempt {attempt}): {e!r}")
            if attempt < max_attempts:
                sleep_time = backoff ** attempt
                if DEBUG_MODE:
                    print(f"[DEBUG] Sleeping {sleep_time}s before retry")
                time.sleep(sleep_time)
            else:
                if DEBUG_MODE:
                    print("[DEBUG] All Gemini upload attempts failed")
    return None

def check_meme(up):
    time.sleep(5)
    prompt = (
            "In this image, is it a product advertisement or an image from a news article? "
            "Strictly answer as instructed:\n"
            "- No extra texts, explanation, description or a reason.\n"
            "- Return only 0 if it is a product advertisement or an image from a news article.\n"
            "- Return 1 if it is a proper meme.\n"
            "I need only a Binary output as instructed. No texts. Only 1 or 0."
    )
    
    resp = model.generate_content([prompt, up])
    if resp.text.strip() == "1":
        print("> (6/10) Meme confirmed")
        return True
    print("❌ Not a meme")
    return False


def generate_caption(up):
    prompt = "Do not ask any question or opinion. No need to give Options either. Give the best Instagram caption for this meme (extremely humorous, relatable, , witty, engaging). Return only the caption"
    try:    
        resp = model.generate_content(
            [prompt, up], generation_config={"temperature": 0.75})
        caption = resp.text.strip()
        print(f"> (7/10) Caption generation successful!")
        return caption
    except Exception as e:
        if DEBUG_MODE:
            print(f"[DEBUG] Caption generation failed: {e!r}")
        return None
