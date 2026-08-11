<p align="center">
  <h1 align="center">🤖 RichMDHelpBot</h1>
  <p align="center">An advanced, asynchronous Telegram Markdown Formatter Bot built using <b>Python 3</b>, <b>aiogram 3.x</b>, <b>aiohttp</b>, and <b>SQLite</b>. It automatically converts custom Markdown syntax into clean Telegram HTML, manages channel footers, and features forced channel subscription.</p>
</p>

<p align="center">
  <a href="https://github.com/MrBoss002/RichMDHelpBot/fork">
    <img src="https://img.shields.io/github/forks/MrBoss002/RichMDHelpBot?style=for-the-badge&logo=github&color=blue" alt="Fork Repo">
  </a>
  <a href="https://github.com/MrBoss002/RichMDHelpBot/stargazers">
    <img src="https://img.shields.io/github/stars/MrBoss002/RichMDHelpBot?style=for-the-badge&logo=github&color=gold" alt="Star Repo">
  </a>
  <a href="https://t.me/RichMDHelpBot">
    <img src="https://img.shields.io/badge/Telegram-Demo%20Bot-26A5E4?style=for-the-badge&logo=telegram" alt="Demo Bot">
  </a>
</p>

---

## ✨ Features

* 📝 **Custom Markdown Engine:** Quickly parse heading tags (`#_`, `##_`, `###_`), bold (`*text*`), italic (`_text_`), and code blocks.
* 📢 **Force Subscription (FSub):** Ensures users join your specified Telegram channel before accessing bot functionality.
* ⚙️ **Interactive Menus:** Seamless navigation using inline keyboards and callbacks.
* ⚡ **Fast & Asynchronous:** Fully non-blocking event loop powered by `aiogram` and `aiohttp`.
* ☁️ **Render Free Tier Ready:** Includes an integrated HTTP port ping server (`10000`) for 24/7 web service deployment.

---

## 🚀 Environment Variables

Create a `.env` file in the root directory (or configure them in your Render dashboard):

| Variable | Description |
| :--- | :--- |
| `BOT_TOKEN` | Your Telegram Bot Token from `@BotFather` |
| `ADMIN_ID` | Your Telegram Numeric User ID |
| `FSUB_CHANNEL_ID` | Required Channel ID (e.g., `-100123456789`) |
| `FSUB_CHANNEL_LINK` | Invite link for the mandatory channel |
| `PORT` | Web server port for Render health checks (default: `10000`) |

---

# 📦 Local Installation

## Clone the repository
```
git clone https://github.com/MrBoss002/RichMDHelpBot.git
cd RichMDHelpBot
```
## Create a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

## Install dependencies
```
pip install -r requirements.txt
```

## Run the bot
```
python main.py
```
---

## ☁️ Deployment on Render

1. Create a new **Web Service** on Render.
2. Connect your GitHub repository: `MrBoss002/RichMDHelpBot`.
3. Choose **Free Tier**.
4. Set execution commands:
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `python main.py`
5. Add your Environment Variables in the Render settings tab and deploy!

---

## 📄 License

- This project is open-source and available under the MIT License.

---


<p align="center">
  <a href="https://t.me/MrBossTG">
    <img src="https://img.shields.io/badge/Main%20Channel-Join%20For%20Updates%20%26%20Releases-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Main Channel">
  </a>
</p>

<p align="center">
  <a href="https://youtube.com/@MrBoss002">
    <img src="https://img.shields.io/badge/YouTube-MrBoss002-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube">
  </a>
  <a href="https://t.me/MrBoss002">
    <img src="https://img.shields.io/badge/Contact-Owner-0088cc?style=for-the-badge&logo=telegram&logoColor=white" alt="Contact Owner">
  </a>
</p>
