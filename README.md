# 🤖 AI-powered Instagram Meme Posting Automation Bot

Check out [ZeekyZoop](https://www.instagram.com/zeekyzoop/) Instagram Page, it is a fully automated pipeline that:

1. **Discovers** trending memes via Google Custom Search (CSE)  
2. **Validates** the image quality and checks if it is a meme.
3. **Uploads** to Google Gemini (LLM) for caption generation.  
4. **Posts** to Instagram via `instagrapi` with session reuse and auto-relogin . 
5. **Quality-Controls** the entire run by sending real-time status updates to your custom **Telegram** bot.

---

## 🔗 Integrations & Architecture

- **Google CSE (Programmable Search)**  
  - Broad web search for PNG memes (or restrict to your favorite domains)  
- **Google Gemini (LLM API)**  
  - AI-driven captioning using a modern LLM, accessed via [Gemini API](https://ai.google.dev/aistudio). 
- **Instagram Automation**  
  - Logs in with a persistent session file, retries on `LoginRequired` exceptions  
- **Telegram Quality Control**  
  - Sends “✅ Success” or “❌ Failure” messages after each major step  
  - Acts as your observability dashboard, so you don’t have to check Instagram manually

---

## 🛡 Reliability & Fault Tolerance

Every external call is wrapped in:

- **Try/Except** blocks  
- **Retry logic** with **exponential backoff** for network blips.  
- **User-Agent spoofing** to avoid CDN blocks. 
- **Strict Boolean returns** (`True`/`False`) so the orchestrator knows exactly what happened.  

This ensures end-to-end stability and clear error reporting.

---

## ⚙️ Quickstart

1. **Clone** the repo  
   ```bash
   git clone https://github.com/your-username/auto-insta-meme.git
   cd auto-insta-meme```

2. **Install** the Dependencies
