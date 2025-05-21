#!/usr/bin/env python3
import sys, time

# Ensure emojis print correctly
sys.stdout.reconfigure(encoding="utf-8")

import google_search as gs
from gemini_client import load_into_gemini, check_meme, generate_caption
from ig_client import IG_login, ig_upload, delete_image
from notifier import send_telegram


def main():
    # ————————————— Start run —————————————
    send_telegram("──────────────────────────")

    # 1–4. Download a meme image
    if not gs.Google_image():
        send_telegram("⚠️ Image download failed. Exiting.")
        return
    send_telegram("1️⃣✔️ Meme downloaded successfully!")

    # Grab the fresh globals off the module
    img_path = gs.image_path
    topic   = gs.searched_topic

    # 5. Upload to Gemini
    upload_ref = load_into_gemini(img_path, topic)
    if not upload_ref:
        send_telegram("⚠️ Upload to Gemini failed. Exiting.")
        return
    send_telegram("2️⃣✔️ Uploaded to Gemini!")

    # 6. Verify it’s a meme
    if not check_meme(upload_ref):
        send_telegram("⚠️ Not a valid meme. Exiting.")
        return
    send_telegram("3️⃣✔️ Meme confirmed by Gemini!")

    # 7. Generate a caption
    caption = generate_caption(upload_ref)
    if not caption:
        send_telegram("⚠️ Caption generation failed. Exiting.")
        return
    send_telegram("4️⃣✔️ Caption generated!")

    # 8. Login to Instagram (or restore session)
    session = IG_login()
    if not session:
        send_telegram("⚠️ Instagram login failed. Exiting.")
        return
    send_telegram("5️⃣✔️ Instagram login successful!")

    # 9. Upload the meme + caption
    if ig_upload(img_path, caption, session):
        send_telegram("✔️ Meme uploaded to Instagram!")
    else:
        send_telegram("⚠️ Instagram upload failed. Exiting.")

    # 10. Clean up local file
    delete_image(img_path)
    send_telegram("7️⃣✔️ Local image deleted!")

    # ————————————— End run —————————————
    send_telegram("──────────────────────────")
    ts = time.strftime("%Y-%m-%d %H:%M:%S %Z%z", time.localtime())
    send_telegram(f"🤖 Meme bot finished running. \n ✅ Meme posted successfully at: {ts}")


if __name__ == "__main__":
    main()
