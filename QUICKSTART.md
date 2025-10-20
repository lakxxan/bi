# ⚡ Quick Start Guide - Telegram Video Bot

## 3 මිනිත්තුවකින් Setup කරන්න! 🚀

### Step 1: Credentials ගන්න (5 min)

#### 1. API_ID සහ API_HASH:
- https://my.telegram.org/apps වලට යන්න
- Phone number එකෙන් login වෙන්න
- "Create application" click කරන්න
- Copy කරගන්න: `api_id` සහ `api_hash`

#### 2. BOT_TOKEN:
- Telegram එකේ @BotFather search කරන්න
- `/newbot` send කරන්න
- Bot name සහ username දෙන්න
- Copy කරගන්න: Bot token

#### 3. CHANNEL_ID:
- Channel එකක් හදන්න or use existing channel
- Bot add කරන්න as Admin
- Username: `@yourchannel`

### Step 2: Google Colab Setup (2 min)

1. **Open Colab**: [colab.research.google.com](https://colab.research.google.com)
2. **Upload files**: `telegram_bot.py` සහ `requirements.txt`
3. **Run cells**:

```python
# Cell 1 - Install
!pip install -q pyrogram TgCrypto

# Cell 2 - Configure
import os
os.environ["API_ID"] = "YOUR_API_ID"
os.environ["API_HASH"] = "YOUR_API_HASH"
os.environ["BOT_TOKEN"] = "YOUR_BOT_TOKEN"
os.environ["CHANNEL_ID"] = "@your_channel"

# Cell 3 - Start Bot
!python telegram_bot.py
```

### Step 3: Use Bot (1 min)

1. Telegram එකේ bot search කරන්න
2. `/start` send කරන්න
3. Video send කරන්න!

---

## 📹 භාවිතය

### Method 1: Video Bot එකට Send කරන්න
- කැමති video bot එකට send කරන්න
- Auto channel එකට upload වෙනවා
- Real-time progress දකින්න පුළුවන්

### Method 2: Colab Storage එකෙන්
```
/upload /content/my_video.mp4
```

---

## ⚡ Speed Tips

### වේගය වැඩි කරගන්න:

1. **TgCrypto use කරන්න** (included!) = 10-20x faster
2. **Colab Pro** = Even faster internet
3. **8 Workers** = Parallel uploads (already configured)

### කොච්චර වේගයද?

| File Size | Upload Time (with TgCrypto) |
|-----------|---------------------------|
| 100 MB    | ~8 seconds                |
| 500 MB    | ~40 seconds               |
| 1 GB      | ~1.5 minutes              |
| 2 GB      | ~3 minutes                |

---

## 🔧 Common Issues

### Bot respond වෙන්නේ නැහැ?
✅ Credentials check කරන්න
✅ Bot token valid ද verify කරන්න
✅ Colab cell run වෙනවද බලන්න

### Upload slow ද?
✅ TgCrypto install වෙලා තියෙනවද: `!pip show TgCrypto`
✅ Colab Pro try කරන්න

### Channel එකට යන්නේ නැහැ?
✅ Bot admin privileges තියෙනවද check කරන්න
✅ Channel username හරි ද verify කරන්න

### ❌ 400 PEER_ID_INVALID fix
මෙම error එක එන්නේ bot එකට channel එක "meet" කරලා නැති නිසා හෝ CHANNEL_ID / permissions වැරදි නිසා.

Steps:
- CHANNEL_ID صحیحද බලන්න: `@yourchannel` හෝ `-100xxxxxxxxxx`
- Bot එක channel එකට Admin ලෙස add කරලා තියෙනවද? (Post Messages permission අවශ්‍යයි)
- Bot එක once channel එකට message එකක් දාලා බලන්න
- Bot තුළ diagnose command එක run කරන්න:
	- `/checkchannel` — CHANNEL_ID resolve කරලා test message එකක් try කරයි, permissions show කරයි

---

## 📞 Need Help?

Full documentation: `README.md` කියවන්න
සියලු features සහ advanced options: `README.md`

---

**දැන් ready! Video upload කරන්න පටන්ගන්න! 🎉**
