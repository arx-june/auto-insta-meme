# src/google_search.py

import os
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from google_images_search import GoogleImagesSearch
from config import JSON_API, CX, DEBUG_MODE

searched_topic = None
image_path = None

def make_retry_session(
    retries: int = 3,
    backoff_factor: float = 1.0,
    status_forcelist: tuple = (429, 502, 503, 504),
) -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    })
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=["GET", "POST"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def Google_image() -> bool:
    """
    1) Picks a random meme topic
    2) Searches Google Images
    3) Downloads one image with retries+timeout
    Returns True on success, False on any error.
    """
    global searched_topic, image_path

    # ── 1) pick topic ────────────────────────────────────────────────────────────────
    topics = [
        "memes","dank memes","humorous memes","brainrot memes","normie memes","classic memes",
        "reddit memes","dark memes","iphone memes","twitter memes","wholesome memes",
        "relatable memes","surreal memes","video memes","vine memes","facebook memes",
        "instagram memes","tiktok memes","political memes","animal memes","gaming memes",
        "reaction memes","advice animal memes","wojak memes","pepe memes","cursed memes",
        "spoof memes","educational memes","anime memes","spongebob memes","historical memes",
        "office memes","work memes","student memes","programmer memes","engineering memes",
        "sports memes","music memes","movie memes","tv show memes","caption memes",
        "baby yoda memes","cat memes","dog memes","food memes","fitness memes",
        "relationship memes","parenting memes","school memes","celebrity memes","tech memes",
        "travel memes","art memes","book memes","science memes","math memes","physics memes",
        "chemistry memes","biology memes","medical memes","law memes","finance memes",
        "economics memes","marketing memes","business memes","startup memes","coding memes",
        "data science memes","AI memes","machine learning memes","robotics memes",
        "space memes","astronomy memes","weather memes","holiday memes","vacation memes",
        "city memes","country memes","language memes","cultural memes","history memes",
        "philosophy memes","psychology memes","sociology memes","politics memes",
        "environmental memes","nature memes","wildlife memes","conservation memes","pet memes",
        "absurd memes","ironic memes","sarcastic memes","pun memes","wordplay memes",
        "viral memes","trending memes","new memes","fresh memes","hilarious memes",
        "best memes","epic memes","make me laugh memes","comedy memes","humor memes",
        "silly memes","goofy memes","quirky memes","witty memes","clever memes","smart memes",
        "intelligent memes","absurdist memes","existential memes","dark humor memes",
        "black humor memes","nerdy memes","geeky memes","awkward memes", "cringe memes"
    ]
    searched_topic = random.choice(topics)
    print(f"> (1/10) Topic: {searched_topic}")

    # ── 2) search ────────────────────────────────────────────────────────────────────
    gis = GoogleImagesSearch(JSON_API, CX)
    params = {
        "q": searched_topic,
        "num": 10,
        "safe": "active",
        "fileType": "png",
    }
    try:
        gis.search(search_params=params)
    except Exception as e:
        if DEBUG_MODE:
            print(f"[DEBUG] GoogleImagesSearch failed: {e!r}")
        return False

    urls = [img.url for img in gis.results()]
    if not urls:
        if DEBUG_MODE:
            print("[DEBUG] No results from GoogleImagesSearch.")
        return False

    subset = random.sample(urls, min(5, len(urls)))
    selected = random.choice(subset)
    print("> (2/10) Image selection successful")

    # ── 3) download with retries + timeout ────────────────────────────────────────────
    image_name = f"{searched_topic}_{random.randint(0,9999)}.png"
    image_path = os.path.join(os.getcwd(), image_name)
    print(f"> (3/10) Downloaded to root directory")

    session = make_retry_session()
    try:
        if DEBUG_MODE:
            print(f"[DEBUG] Attempting download from: {selected}")
        resp = session.get(selected, stream=True, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as e:
        if DEBUG_MODE:
            print(f"[DEBUG] Image download failed ({selected}): {e!r}")
        return False

    # ── write file ───────────────────────────────────────────────────────────────────
    try:
        with open(image_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        if DEBUG_MODE:
            print(f"[DEBUG] Error writing image to disk: {e!r}")
        return False

    print("> (4/10) Download complete")
    return True
