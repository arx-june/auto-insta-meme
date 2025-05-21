# src/ig_client.py
import os
from config import IG_USERNAME, IG_PASSWORD, SESSION_FILE, DEBUG_MODE
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from instagrapi import Client
# Import relevant exceptions
from instagrapi.exceptions import (
    ChallengeRequired,
    LoginRequired,
)


# Your IG_login function (leaving it as is from your provided code for now)
def IG_login():
    """
    Load or refresh an Instagrapi session, handling challenges if needed.
    """
    cl = Client()
    if DEBUG_MODE:
        print(f"[DEBUG] SESSION_FILE = {SESSION_FILE}")
        print(f"[DEBUG] Exists before load? {os.path.isfile(SESSION_FILE)}")

    if os.path.isfile(SESSION_FILE):
        cl.load_settings(SESSION_FILE)
        cookies = cl.cookie_dict
        if DEBUG_MODE:
            print(f"[DEBUG] Number of cookies loaded: {len(cookies)}")
            print(f"[DEBUG] csrftoken present? {'csrftoken' in cookies}")
    else:
        # This print statement was missing in your original snippet, adding for completeness
        if DEBUG_MODE:
            print(f"[DEBUG] No session file found at {SESSION_FILE}, creating a new one.")


    try:
        cl.login(IG_USERNAME, IG_PASSWORD)
        print("> (8/10) Instagram login (or session reuse) successful.")
    except ChallengeRequired:
        code = input("Enter challenge code sent to email/phone: ")
        cl.challenge_code_handler(code)
        # It's good practice to try logging in again after handling challenge
        cl.login(IG_USERNAME, IG_PASSWORD)
        print("> (8/10) Challenge passed, login complete.")
    except Exception as e:
        print(f"> Error during initial login: {e}")
        return None # Indicate failure

    try:
        cl.get_timeline_feed()
    except LoginRequired:
        print("> Session invalid after login attempt. Trying fresh login.")
        cl.logout()
        try:
            cl.login(IG_USERNAME, IG_PASSWORD)
            print("> (8/10) Fresh login successful after logout.")
        except Exception as e_fresh:
            print(f"> Error during fresh login: {e_fresh}")
            return None # Indicate failure
    except Exception as e_verify:
        print(f"> Error verifying session with get_timeline_feed: {e_verify}")
        # Depending on severity, you might return None here too.

    os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
    cl.dump_settings(SESSION_FILE)
    if DEBUG_MODE: # Corrected DEBUG_MODE check
        # Ensure file exists before getting size to avoid error if dump failed
        if os.path.isfile(SESSION_FILE):
            size = os.path.getsize(SESSION_FILE)
            print(f"[DEBUG] session.json size after dump: {size} bytes")
        else:
            print(f"[DEBUG] Session file {SESSION_FILE} not found after dump attempt.")
    return cl


# --- CORRECTED ig_upload ---
def ig_upload(image_path, caption, cl: Client):
    """
    Upload a photo, retrying once on login failure.
    Returns True on success, False on failure.
    """
    # Import specific exception for upload context
    from instagrapi.exceptions import LoginRequired as UploadLoginRequired

    try:
        media = cl.photo_upload(path=image_path, caption=caption)
        # instagrapi's photo_upload returns a Media object on success.
        # A Media object is "truthy".
        if media:
            print("> (9/10) Uploaded to Instagram.")
            return True
        else:
            # This case is less likely if photo_upload always raises an exception on failure,
            # but it's a good safeguard.
            print("> (9/10) Upload to Instagram: photo_upload returned a falsy value (e.g., None) without erroring.")
            return False
    except UploadLoginRequired:
        print("> Error: Upload failed due to invalid session. Re-logging in…")
        try:
            # Get a new client instance with a fresh login.
            # The 'cl' parameter of this function is local; re-assigning it here
            # doesn't change the 'session' variable in main.py.
            # IG_login() should return a client object or None/raise error on failure.
            new_cl_session = IG_login()
            if not new_cl_session: # If IG_login indicated failure
                print("> Error: Re-login attempt failed during upload retry.")
                return False

            media_retry = new_cl_session.photo_upload(path=image_path, caption=caption)
            if media_retry:
                print("> (9/10) Uploaded to Instagram after re-login.")
                return True
            else:
                print("> (9/10) Upload to Instagram after re-login: photo_upload returned a falsy value.")
                return False
        except Exception as e_retry: # Catch any error during re-login or second upload attempt
            print(f"> Error during upload retry: {e_retry}")
            return False
    except (MediaUploadError, MediaNotUpload) as e_media: # Catch specific upload errors
        print(f"> Error: Instagram media upload failed directly: {e_media}")
        return False
    except Exception as e: # Catch any other unexpected errors during the first upload attempt
        print(f"> Error: An unexpected error occurred during Instagram upload: {e}")
        return False


def delete_image(image_path):
    try:
        os.remove(image_path)
        print("> (10/10) Local file deleted.")
    except OSError as e: # Be more specific with file operation errors
        print(f"> Error deleting local file {image_path}: {e}")
    print("_________________________________________")