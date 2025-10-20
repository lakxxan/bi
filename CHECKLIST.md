# ✅ Setup Checklist - Telegram Video Bot

ඔයාගේ bot එක setup කරන්න මේ checklist එක follow කරන්න! 📋

---

## 📝 Pre-Setup (5 minutes)

### ☐ Step 1: Get API Credentials

#### 1.1 Get API_ID and API_HASH:
- [ ] Visit https://my.telegram.org/apps
- [ ] Login with your phone number
- [ ] Click "API development tools"
- [ ] Fill in application details:
  - [ ] App title: (e.g., "My Video Bot")
  - [ ] Short name: (e.g., "videobot")
  - [ ] Platform: Select any
- [ ] Click "Create application"
- [ ] Copy and save:
  - [ ] `api_id` (numbers only)
  - [ ] `api_hash` (long string)

#### 1.2 Get BOT_TOKEN:
- [ ] Open Telegram app
- [ ] Search for @BotFather
- [ ] Send `/start` command
- [ ] Send `/newbot` command
- [ ] Provide bot name (e.g., "My Video Upload Bot")
- [ ] Provide bot username (must end with 'bot', e.g., "my_video_bot")
- [ ] Copy the bot token (format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
- [ ] Save token securely

#### 1.3 Create/Setup Channel (Optional):
- [ ] Create a new Telegram channel (or use existing)
- [ ] Go to channel settings → Administrators
- [ ] Click "Add Administrator"
- [ ] Search for your bot username
- [ ] Add bot as administrator
- [ ] Enable "Post Messages" permission
- [ ] Note down channel username (e.g., `@mychannel`)

---

## 🚀 Setup (3 minutes)

### ☐ Step 2: Google Colab Setup

#### 2.1 Open Google Colab:
- [ ] Visit https://colab.research.google.com
- [ ] Sign in with Google account

#### 2.2 Upload Bot Files:
- [ ] Click on folder icon (left sidebar)
- [ ] Upload these files:
  - [ ] `telegram_bot.py`
  - [ ] `requirements.txt`
- [ ] Verify files are uploaded

#### 2.3 Create New Notebook:
- [ ] Click "New notebook" or upload `colab_setup.ipynb`
- [ ] Rename notebook (e.g., "Telegram Bot")

---

## ⚙️ Configuration (2 minutes)

### ☐ Step 3: Install Dependencies

```python
# Run this cell:
!pip install -q pyrogram TgCrypto
```

- [ ] Run the cell (Shift + Enter)
- [ ] Wait for installation to complete
- [ ] Verify: "Successfully installed" message appears

---

### ☐ Step 4: Configure Bot

```python
# Run this cell with YOUR credentials:
import os

os.environ["API_ID"] = "12345678"  # ← Your API ID here
os.environ["API_HASH"] = "abcd1234..."  # ← Your API Hash here
os.environ["BOT_TOKEN"] = "123456:ABC..."  # ← Your Bot Token here
os.environ["CHANNEL_ID"] = "@yourchannel"  # ← Your Channel (optional)

print("✅ Configuration complete!")
```

**Important:** Replace with YOUR actual values!

- [ ] Replace `API_ID` with your api_id
- [ ] Replace `API_HASH` with your api_hash
- [ ] Replace `BOT_TOKEN` with your bot token
- [ ] Replace `CHANNEL_ID` with your channel (or leave empty)
- [ ] Run the cell
- [ ] Verify: "✅ Configuration complete!" appears

---

### ☐ Step 5: Test Setup (Optional but Recommended)

```python
# Run this cell:
!python test_setup.py
```

- [ ] Run the test script
- [ ] Check for ✅ marks (all should be green)
- [ ] If ❌ appears, fix the issues
- [ ] Verify connection test passes

---

## 🎮 Launch (1 minute)

### ☐ Step 6: Start Bot

```python
# Run this cell:
!python telegram_bot.py
```

- [ ] Run the cell
- [ ] Wait for "Bot is running!" message
- [ ] Keep this cell running
- [ ] Don't close the browser tab

---

## ✨ Testing (2 minutes)

### ☐ Step 7: Test Bot Functionality

#### 7.1 Basic Test:
- [ ] Open Telegram app
- [ ] Search for your bot username
- [ ] Click on the bot
- [ ] Send `/start` command
- [ ] Verify: Welcome message appears

#### 7.2 Status Check:
- [ ] Send `/status` command
- [ ] Verify: Bot shows as "Online"
- [ ] Check: Worker count = 8
- [ ] Check: TgCrypto = Enabled

#### 7.3 File Upload Test:
- [ ] Send a small video file (< 10MB) to test
- [ ] Verify: Bot starts downloading
- [ ] Verify: Progress updates appear
- [ ] Verify: Upload completes successfully
- [ ] Check: Video appears in channel (if configured)

---

## 🎯 Advanced Testing (Optional)

### ☐ Step 8: Large File Test

- [ ] Prepare a large video file (>100MB)
- [ ] Send to bot
- [ ] Monitor progress:
  - [ ] Download speed shown
  - [ ] Upload speed shown
  - [ ] ETA calculated
  - [ ] Percentage updates
- [ ] Verify: Completes successfully
- [ ] Check: Streaming works (play while uploading)

---

## 📊 Performance Verification

### ☐ Step 9: Speed Test

Test upload speeds with different file sizes:

| File Size | Expected Time (with TgCrypto) | Your Time | Status |
|-----------|------------------------------|-----------|--------|
| 10 MB     | ~1 second                    | _____     | ☐      |
| 50 MB     | ~5 seconds                   | _____     | ☐      |
| 100 MB    | ~8 seconds                   | _____     | ☐      |
| 500 MB    | ~40 seconds                  | _____     | ☐      |
| 1 GB      | ~1.5 minutes                 | _____     | ☐      |

**Note:** Times vary based on internet speed

---

## 🔧 Troubleshooting

### Common Issues Checklist:

#### Issue: Bot not responding
- [ ] Check: Is the bot cell still running?
- [ ] Check: Are credentials correct?
- [ ] Check: Is bot token valid? (check @BotFather)
- [ ] Try: Restart the bot cell

#### Issue: Slow uploads
- [ ] Check: Is TgCrypto installed? (`!pip show TgCrypto`)
- [ ] Check: Internet connection speed
- [ ] Try: Use Colab Pro for better speeds
- [ ] Try: Close other bandwidth-heavy apps

#### Issue: Can't upload to channel
- [ ] Check: Is bot admin in channel?
- [ ] Check: Does bot have "Post Messages" permission?
- [ ] Check: Is channel username correct? (format: `@channel`)
- [ ] Try: Use channel ID instead of username

#### Issue: "File not found" error
- [ ] Check: File path is correct
- [ ] Check: File is in `/content/` directory
- [ ] Check: File name has no special characters
- [ ] Try: Upload file again to Colab

---

## 🎉 Success Criteria

Your bot is fully working if:

- ✅ Bot responds to `/start` command
- ✅ Bot shows online in `/status`
- ✅ Can send small files successfully
- ✅ Can send large files (>500MB)
- ✅ Progress updates work correctly
- ✅ Upload speed is > 5 MB/s
- ✅ Videos have streaming enabled
- ✅ Channel uploads work (if configured)

---

## 📚 Next Steps After Setup

Once setup is complete:

### Learn More:
- [ ] Read full `README.md`
- [ ] Check `ARCHITECTURE.md` for technical details
- [ ] Review `PACKAGE_INFO.md` for features

### Customize:
- [ ] Change worker count for your needs
- [ ] Modify progress update messages
- [ ] Add custom captions
- [ ] Implement additional features

### Deploy:
- [ ] Consider Colab Pro for 24/7 operation
- [ ] Or deploy to VPS/server
- [ ] Set up monitoring
- [ ] Add error logging

### Use Daily:
- [ ] Upload your video collection
- [ ] Share content to channel
- [ ] Archive important videos
- [ ] Enjoy fast uploads! 🚀

---

## 📞 Help & Support

If you're stuck:

1. **Re-read the documentation:**
   - [ ] QUICKSTART.md - Quick setup
   - [ ] README.md - Full guide
   - [ ] This checklist again

2. **Run diagnostics:**
   ```python
   !python test_setup.py
   ```

3. **Check logs:**
   - Look at Colab output for errors
   - Check Telegram bot chat for error messages

4. **Common fixes:**
   - Restart Colab runtime
   - Reinstall dependencies
   - Double-check credentials
   - Test with smaller files first

---

## ✅ Completion Status

Mark your progress:

- [ ] ✅ All credentials obtained
- [ ] ✅ Colab setup complete
- [ ] ✅ Dependencies installed
- [ ] ✅ Bot configured
- [ ] ✅ Test script passed
- [ ] ✅ Bot launched successfully
- [ ] ✅ Basic tests completed
- [ ] ✅ Large file test completed
- [ ] ✅ Performance verified
- [ ] ✅ Ready for daily use!

---

**🎊 Congratulations! ඔයාගේ bot එක දැන් ready! 🎊**

Enjoy fast video uploads! 🚀📹
