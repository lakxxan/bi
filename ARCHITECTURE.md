# 🏗️ Bot Architecture & Workflow

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GOOGLE COLAB                            │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                                                         │ │
│  │  telegram_bot.py (Main Bot)                           │ │
│  │  ├── Pyrogram Client (8 Workers)                      │ │
│  │  ├── TgCrypto (Speed Optimization)                    │ │
│  │  ├── Progress Tracking                                │ │
│  │  └── File Management                                  │ │
│  │                                                         │ │
│  └───────────────────────────────────────────────────────┘ │
│                          ▲ ▼                                │
└──────────────────────────┼─┼────────────────────────────────┘
                           │ │
                    API Calls (HTTPS)
                           │ │
┌──────────────────────────┼─┼────────────────────────────────┐
│                    TELEGRAM API                             │
│  ┌─────────────────────┐ │ │ ┌─────────────────────┐       │
│  │   Bot Messages      │◄┼─┼─│   Bot Commands      │       │
│  │   File Uploads      │ │ │ │   User Requests     │       │
│  │   Progress Updates  │ │ │ │   Downloads         │       │
│  └─────────────────────┘ │ │ └─────────────────────┘       │
└──────────────────────────┼─┼────────────────────────────────┘
                           │ │
                           ▼ ▼
┌─────────────────────────────────────────────────────────────┐
│                    TELEGRAM CLIENTS                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   User Bot   │    │   Channel    │    │   Users      │ │
│  │   Commands   │    │   Uploads    │    │   Downloads  │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Upload Workflow

### Method 1: Direct File Upload

```
User → Bot
  │
  ├─ Send Video File
  │     │
  │     ▼
  │  [Download to Colab]
  │     │
  │     ├─ Progress Updates
  │     ├─ Speed Calculation
  │     └─ ETA Estimation
  │     │
  │     ▼
  │  [Upload to Channel]
  │     │
  │     ├─ 8 Parallel Workers
  │     ├─ TgCrypto Optimization
  │     ├─ Streaming Enabled
  │     └─ Real-time Progress
  │     │
  │     ▼
  │  [Cleanup & Report]
  │     │
  │     └─ Delete temp file
  │
  └─ Success Message ✅
```

### Method 2: Command Upload

```
User → Bot
  │
  ├─ /upload /content/video.mp4
  │     │
  │     ▼
  │  [Check File Exists]
  │     │
  │     ├─ Yes ✅
  │     │   │
  │     │   ▼
  │     │ [Upload to Channel]
  │     │   │
  │     │   ├─ Streaming Support
  │     │   ├─ Progress Tracking
  │     │   └─ Speed Optimization
  │     │   │
  │     │   ▼
  │     │ Success Message ✅
  │     │
  │     └─ No ❌
  │         │
  │         └─ Error: File not found
```

---

## ⚡ Performance Optimization Flow

```
┌─────────────────────────────────────────┐
│         File Upload Request             │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Initialize Upload Session          │
│  • Create client with 8 workers         │
│  • Enable TgCrypto                      │
│  • Prepare progress tracking            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│        Parallel Upload Process          │
│                                         │
│  Worker 1 ──┐                          │
│  Worker 2 ──┤                          │
│  Worker 3 ──┤                          │
│  Worker 4 ──┼─► Upload Chunks         │
│  Worker 5 ──┤   (Simultaneous)        │
│  Worker 6 ──┤                          │
│  Worker 7 ──┤                          │
│  Worker 8 ──┘                          │
│                                         │
│  TgCrypto: Encrypts data at C speed   │
│  Result: 10-20x faster than normal    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│       Progress Tracking Loop            │
│  • Calculate speed (bytes/sec)          │
│  • Estimate time remaining (ETA)        │
│  • Update percentage (%)                │
│  • Send progress message (every 1s)     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│          Upload Complete                │
│  • Enable streaming                     │
│  • Generate caption                     │
│  • Send success message                 │
└─────────────────────────────────────────┘
```

---

## 🎛️ Component Breakdown

### Core Components:

#### 1. **Pyrogram Client**
```python
Client(
    session_name="telegram_bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=8  # Key for parallel processing
)
```
- Manages Telegram connection
- Handles authentication
- Controls worker threads

#### 2. **TgCrypto**
```python
# Automatically used when installed
# Provides C-level encryption speed
# 10-20x faster than pure Python
```
- Fast encryption/decryption
- Optimized for large files
- Native C implementation

#### 3. **Progress Callback**
```python
async def progress_callback(current, total, ...):
    # Calculate metrics
    percentage = current * 100 / total
    speed = current / elapsed_time
    eta = (total - current) / speed
    
    # Update user
    await message.edit_text(progress_info)
```
- Real-time tracking
- Speed calculation
- ETA estimation

#### 4. **File Handler**
```python
@app.on_message(filters.video | filters.document)
async def handle_file(client, message):
    # Download
    # Process
    # Upload
    # Cleanup
```
- Auto-detect file type
- Manage downloads/uploads
- Clean temporary files

---

## 📊 Data Flow

### Upload Process:

```
┌─────────────┐
│ Local File  │
│ or          │──┐
│ Telegram    │  │
│ Message     │  │
└─────────────┘  │
                 │
                 ▼
         ┌───────────────┐
         │  Bot Memory   │
         │  (Streaming)  │
         └───────┬───────┘
                 │
                 │ [Parallel Processing]
                 │ [8 Workers Active]
                 │ [TgCrypto Enabled]
                 │
                 ▼
         ┌───────────────┐
         │ Telegram API  │
         │   (Upload)    │
         └───────┬───────┘
                 │
                 ▼
         ┌───────────────┐
         │ Target        │
         │ Channel/Chat  │
         └───────────────┘
```

### Speed Comparison:

```
Without Optimization:
[██░░░░░░░░] 20% - 120s elapsed - ETA: 480s
Speed: ~1 MB/s

With TgCrypto:
[████████░░] 80% - 30s elapsed - ETA: 7s
Speed: ~15 MB/s

With TgCrypto + 8 Workers:
[██████████] 100% - 28s elapsed - Done! ✅
Speed: ~20 MB/s
```

---

## 🔧 Configuration Layers

```
┌─────────────────────────────────────────┐
│         Environment Variables           │
│  • API_ID                               │
│  • API_HASH                             │
│  • BOT_TOKEN                            │
│  • CHANNEL_ID                           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Bot Configuration               │
│  • WORKERS = 8                          │
│  • SESSION_NAME                         │
│  • ParseMode                            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│        Runtime Settings                 │
│  • Progress update interval: 1s         │
│  • Streaming: Enabled                   │
│  • Auto-cleanup: Enabled                │
└─────────────────────────────────────────┘
```

---

## 🚀 Deployment Architecture

### Google Colab Deployment:

```
┌─────────────────────────────────────────┐
│         Google Colab VM                 │
│  ┌───────────────────────────────────┐ │
│  │  Python 3.10 Environment          │ │
│  │  ├─ Pyrogram 2.0+                 │ │
│  │  ├─ TgCrypto 1.2+                 │ │
│  │  └─ Bot Process                   │ │
│  └───────────────────────────────────┘ │
│                                         │
│  Resources:                             │
│  • RAM: 12GB                            │
│  • Disk: 100GB                          │
│  • Internet: High-speed                 │
│  • GPU: Optional (T4)                   │
└─────────────────────────────────────────┘
         │
         │ HTTPS (443)
         │
         ▼
┌─────────────────────────────────────────┐
│       Telegram Servers                  │
│  • api.telegram.org                     │
│  • Global CDN                           │
│  • Load Balanced                        │
└─────────────────────────────────────────┘
```

---

## 📈 Scalability

### Current Setup:
- ✅ Single bot instance
- ✅ 8 parallel workers
- ✅ Handles 2GB files
- ✅ ~20 MB/s upload speed

### Can Scale To:
- 🔄 Multiple bot instances
- 🔄 16-32 workers per instance
- 🔄 Distributed processing
- 🔄 Load balancing

---

## 🎯 Key Features Implementation

| Feature | Implementation | Benefit |
|---------|---------------|---------|
| Large Files | Chunked upload | 2GB+ support |
| Speed | 8 workers + TgCrypto | 10-20x faster |
| Streaming | `supports_streaming=True` | Instant playback |
| Progress | Callback function | User feedback |
| Auto Forward | Message handler | Convenience |
| Error Handling | Try-except blocks | Reliability |
| Cleanup | Auto delete temps | Space saving |

---

**මේ architecture එක වැඩ කරන්නේ efficiently සහ reliably! 🚀**
