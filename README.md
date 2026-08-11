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
  
  <div align="center">
  <h2>📬 Developer Space</h2>
  <p>Need help, want to report a bug, or connect with the developer?</p>

  <p>
    <a href="https://t.me/MrBossTG">
      <img src="https://img.shields.io/badge/Main%20Channel%20Join%20For%20Updates%20%26%20Releases-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Main Channel" />
    </a>
  </p>

  <p>
    <a href="https://t.me/MrBoss002">
      <img src="https://img.shields.io/badge/💬%20Help%20%26%20Feedback%20Contact%20Admin-1613ad?style=for-the-badge&logo=telegram&logoColor=white" alt="Help and Feedback" />
    </a>
    &nbsp;&nbsp;
    <a href="https://sites.google.com/view/zerotwo-onlinestore">
      <img src="https://img.shields.io/badge/🛍️%20ZeroTwo%20Store%20Catalog-13ad7c?style=for-the-badge&logo=google-chrome&logoColor=white" alt="ZeroTwo Store" />
    </a>
  </p>

  <p>
    <a href="https://youtube.com/@MrBoss002">
      <img src="https://img.shields.io/badge/YouTube%20MrBoss002-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube" />
    </a>
  </p>

  <p>
    Developed with ❤️ by <b>Muhammad Risvan C</b> (<a href="https://github.com/MrBoss002">@MrBoss002</a>)
  </p>
</div>
