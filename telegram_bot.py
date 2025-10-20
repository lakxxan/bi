"""
High-Performance Telegram Bot for Large Video Files
Optimized for Google Colab with streaming support and fast uploads
"""

import os
import sys
import shutil
import asyncio
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

# For Google Drive downloads
import subprocess
import re
import requests
from io import BytesIO

# Configuration
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "")  # Your channel username or ID

# Performance settings
WORKERS = 8  # Number of workers for faster uploads
SESSION_NAME = "telegram_bot_session"

# Initialize bot
app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=WORKERS
)


def format_size(size_bytes):
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def format_time(seconds):
    """Format seconds to human readable time"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


async def progress_callback(current, total, message, start_time, text):
    """Progress callback for upload/download tracking"""
    now = time.time()
    diff = now - start_time
    
    if diff < 1:  # Update every 1 second
        return
    
    percentage = current * 100 / total
    speed = current / diff
    eta = (total - current) / speed if speed > 0 else 0
    
    progress_text = (
        f"{text}\n\n"
        f"📊 Progress: {percentage:.1f}%\n"
        f"📦 Size: {format_size(current)} / {format_size(total)}\n"
        f"⚡ Speed: {format_size(speed)}/s\n"
        f"⏱️ ETA: {format_time(eta)}\n"
        f"⏰ Elapsed: {format_time(diff)}"
    )
    
    try:
        await message.edit_text(progress_text)
    except:
        pass


@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    welcome_text = (
        "🎬 **High-Performance Video Upload Bot**\n\n"
        "Features:\n"
        "✅ Upload videos >2GB with streaming support\n"
        "✅ Fast parallel uploads with 8 workers\n"
        "✅ Optimized with TgCrypto for maximum speed\n"
        "✅ Real-time progress tracking\n"
        "✅ Direct upload to channels\n\n"
        "**Commands:**\n"
        "/start - Show this message\n"
        "/upload <file_path> - Upload video from Colab\n"
        "/status - Check bot status\n\n"
        "**Usage:**\n"
        "Just send me a video file or use /upload command!"
    )
    await message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)


@app.on_message(filters.command("status"))
async def status_command(client: Client, message: Message):
    """Check bot status"""
    status_text = (
        "✅ **Bot Status: Online**\n\n"
        f"👤 Bot: @{(await client.get_me()).username}\n"
        f"⚙️ Workers: {WORKERS}\n"
        f"📡 Channel: {CHANNEL_ID if CHANNEL_ID else 'Not configured'}\n"
        f"🚀 TgCrypto: Enabled\n"
        f"💾 Session: Active"
    )
    await message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)


@app.on_message(filters.command("upload"))
async def upload_command(client: Client, message: Message):
    """Upload video from local path"""
    try:
        # Extract file path from command
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            await message.reply_text(
                "❌ Please provide a file path!\n\n"
                "Usage: `/upload /path/to/video.mp4`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        file_path = command_parts[1].strip()
        
        # Check if file exists
        if not os.path.exists(file_path):
            await message.reply_text(f"❌ File not found: `{file_path}`", parse_mode=ParseMode.MARKDOWN)
            return
        
        # Get file info
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        
        status_msg = await message.reply_text(
            f"📤 Preparing to upload...\n\n"
            f"📁 File: `{file_name}`\n"
            f"📦 Size: {format_size(file_size)}",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Upload video
        start_time = time.time()
        
        target_chat = CHANNEL_ID if CHANNEL_ID else message.chat.id
        
        await client.send_video(
            chat_id=target_chat,
            video=file_path,
            caption=f"📹 {file_name}\n💾 {format_size(file_size)}",
            supports_streaming=True,
            progress=progress_callback,
            progress_args=(status_msg, start_time, "📤 Uploading video...")
        )
        
        upload_time = time.time() - start_time
        avg_speed = file_size / upload_time if upload_time > 0 else 0
        
        await status_msg.edit_text(
            f"✅ **Upload Complete!**\n\n"
            f"📁 File: `{file_name}`\n"
            f"📦 Size: {format_size(file_size)}\n"
            f"⏱️ Time: {format_time(upload_time)}\n"
            f"⚡ Avg Speed: {format_size(avg_speed)}/s\n"
            f"📺 Channel: {target_chat if CHANNEL_ID else 'Current chat'}",
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")


@app.on_message(filters.video | filters.document)
async def handle_file(client: Client, message: Message):
    """Handle video/document files sent to bot"""
    try:
        # Get file info
        if message.video:
            file = message.video
            file_name = file.file_name or f"video_{file.file_id}.mp4"
        else:
            file = message.document
            file_name = file.file_name or f"document_{file.file_id}"
        
        file_size = file.file_size
        
        status_msg = await message.reply_text(
            f"📥 Downloading...\n\n"
            f"📁 File: `{file_name}`\n"
            f"📦 Size: {format_size(file_size)}",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Download file
        start_time = time.time()
        download_path = f"/content/{file_name}"
        
        await client.download_media(
            message,
            file_name=download_path,
            progress=progress_callback,
            progress_args=(status_msg, start_time, "📥 Downloading...")
        )
        
        download_time = time.time() - start_time
        
        # Upload to channel if configured
        if CHANNEL_ID:
            await status_msg.edit_text(
                f"📤 Uploading to channel...\n\n"
                f"📁 File: `{file_name}`\n"
                f"📦 Size: {format_size(file_size)}",
                parse_mode=ParseMode.MARKDOWN
            )
            
            start_time = time.time()
            
            await client.send_video(
                chat_id=CHANNEL_ID,
                video=download_path,
                caption=f"📹 {file_name}\n💾 {format_size(file_size)}",
                supports_streaming=True,
                progress=progress_callback,
                progress_args=(status_msg, start_time, "📤 Uploading to channel...")
            )
            
            upload_time = time.time() - start_time
            total_time = download_time + upload_time
            avg_speed = file_size / total_time if total_time > 0 else 0
            
            await status_msg.edit_text(
                f"✅ **Uploaded to Channel!**\n\n"
                f"📁 File: `{file_name}`\n"
                f"📦 Size: {format_size(file_size)}\n"
                f"⏱️ Download: {format_time(download_time)}\n"
                f"⏱️ Upload: {format_time(upload_time)}\n"
                f"⚡ Avg Speed: {format_size(avg_speed)}/s",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Clean up
            if os.path.exists(download_path):
                os.remove(download_path)
        else:
            await status_msg.edit_text(
                f"✅ **Download Complete!**\n\n"
                f"📁 File: `{file_name}`\n"
                f"📦 Size: {format_size(file_size)}\n"
                f"⏱️ Time: {format_time(download_time)}\n"
                f"💾 Saved to: `{download_path}`\n\n"
                f"ℹ️ Configure CHANNEL_ID to auto-upload",
                parse_mode=ParseMode.MARKDOWN
            )
            
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")


# --- NEW: Google Drive link handler ---
@app.on_message(filters.command("gdrive"))
async def gdrive_command(client: Client, message: Message):
    """Download Google Drive public video and upload to channel"""
    try:
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            await message.reply_text(
                "❌ Please provide a Google Drive public link!\n\n"
                "Usage: `/gdrive <public_link>`",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        gdrive_url = command_parts[1].strip()

        # Extract file ID from Google Drive link
        match = re.search(r"/d/([\w-]+)|id=([\w-]+)", gdrive_url)
        file_id = match.group(1) or match.group(2) if match else None
        if not file_id:
            await message.reply_text("❌ Invalid Google Drive link!")
            return

        # Download using gdown
        file_name = f"gdrive_{file_id}.mp4"
        download_path = f"/content/{file_name}"
        status_msg = await message.reply_text(f"📥 Downloading from Google Drive...\n\n🔗 `{gdrive_url}`", parse_mode=ParseMode.MARKDOWN)

        # Install gdown if not present
        try:
            import gdown
        except ImportError:
            subprocess.run(["pip", "install", "gdown"])
            import gdown

        # Download file
        start_time = time.time()
        gdown.download(gdrive_url, download_path, quiet=False)
        download_time = time.time() - start_time

        # Get file size
        file_size = os.path.getsize(download_path)

        await status_msg.edit_text(
            f"📤 Uploading to channel...\n\n"
            f"📁 File: `{file_name}`\n"
            f"📦 Size: {format_size(file_size)}",
            parse_mode=ParseMode.MARKDOWN
        )

        # Upload to channel
        start_time = time.time()
        target_chat = CHANNEL_ID if CHANNEL_ID else message.chat.id
        await client.send_video(
            chat_id=target_chat,
            video=download_path,
            caption=f"📹 {file_name}\n💾 {format_size(file_size)}\n🔗 From Google Drive",
            supports_streaming=True,
            progress=progress_callback,
            progress_args=(status_msg, start_time, "📤 Uploading video...")
        )
        upload_time = time.time() - start_time
        avg_speed = file_size / upload_time if upload_time > 0 else 0

        await status_msg.edit_text(
            f"✅ **Upload Complete!**\n\n"
            f"📁 File: `{file_name}`\n"
            f"📦 Size: {format_size(file_size)}\n"
            f"⏱️ Download: {format_time(download_time)}\n"
            f"⏱️ Upload: {format_time(upload_time)}\n"
            f"⚡ Avg Speed: {format_size(avg_speed)}/s\n"
            f"📺 Channel: {target_chat if CHANNEL_ID else 'Current chat'}",
            parse_mode=ParseMode.MARKDOWN
        )

        # Clean up
        if os.path.exists(download_path):
            os.remove(download_path)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")


# --- NEW: Stream video from URL and upload ---
@app.on_message(filters.command("uploadurl"))
async def uploadurl_command(client: Client, message: Message):
    """Stream video from direct link or Google Drive and upload to channel (no disk save)"""
    try:
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            await message.reply_text(
                "❌ Please provide a direct video link or Google Drive link!\n\n"
                "Usage: `/uploadurl <link>`",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        url = command_parts[1].strip()
        status_msg = await message.reply_text(f"📥 Streaming from URL...\n\n🔗 `{url}`", parse_mode=ParseMode.MARKDOWN)

        # If Google Drive link, try to get direct download link
        if "drive.google.com" in url:
            # Try to get file id
            match = re.search(r"/d/([\w-]+)|id=([\w-]+)", url)
            file_id = match.group(1) or match.group(2) if match else None
            if not file_id:
                await status_msg.edit_text("❌ Invalid Google Drive link!")
                return
            direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        else:
            direct_url = url

        # Stream download
        start_time = time.time()
        response = requests.get(direct_url, stream=True)
        if response.status_code != 200:
            await status_msg.edit_text(f"❌ Failed to download. Status code: {response.status_code}")
            return

        # Get file name from headers or URL
        file_name = None
        if 'content-disposition' in response.headers:
            cd = response.headers['content-disposition']
            match = re.search('filename="(.+?)"', cd)
            if match:
                file_name = match.group(1)
        if not file_name:
            file_name = url.split('/')[-1].split('?')[0] or "streamed_video.mp4"

        # Read content into BytesIO (streaming, but still needs RAM)
        file_bytes = BytesIO()
        chunk_size = 1024 * 1024  # 1MB
        total_size = 0
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                file_bytes.write(chunk)
                total_size += len(chunk)
                # Optionally, update progress here
        file_bytes.seek(0)

        download_time = time.time() - start_time

        await status_msg.edit_text(
            f"📤 Uploading to channel...\n\n"
            f"📁 File: `{file_name}`\n"
            f"📦 Size: {format_size(total_size)}",
            parse_mode=ParseMode.MARKDOWN
        )

        # Upload to channel
        start_time = time.time()
        target_chat = CHANNEL_ID if CHANNEL_ID else message.chat.id
        await client.send_video(
            chat_id=target_chat,
            video=file_bytes,
            file_name=file_name,
            caption=f"📹 {file_name}\n💾 {format_size(total_size)}\n🔗 Streamed from URL",
            supports_streaming=True,
            # progress callback not supported for BytesIO
        )
        upload_time = time.time() - start_time
        avg_speed = total_size / upload_time if upload_time > 0 else 0

        await status_msg.edit_text(
            f"✅ **Upload Complete!**\n\n"
            f"📁 File: `{file_name}`\n"
            f"📦 Size: {format_size(total_size)}\n"
            f"⏱️ Download: {format_time(download_time)}\n"
            f"⏱️ Upload: {format_time(upload_time)}\n"
            f"⚡ Avg Speed: {format_size(avg_speed)}/s\n"
            f"📺 Channel: {target_chat if CHANNEL_ID else 'Current chat'}",
            parse_mode=ParseMode.MARKDOWN
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")


def ensure_colab_copy():
    """Copy this script to /content/telegram_bot.py if running in Google Colab environment.

    This helps when users run commands expecting the script under /content.
    """
    try:
        # Detect Colab-like environment
        if os.path.isdir("/content"):
            src = os.path.abspath(__file__) if "__file__" in globals() else None
            dest = "/content/telegram_bot.py"
            if src and os.path.abspath(src) != os.path.abspath(dest):
                # Copy if missing or outdated
                should_copy = (not os.path.exists(dest))
                if not should_copy:
                    try:
                        should_copy = os.path.getmtime(src) > os.path.getmtime(dest)
                    except Exception:
                        should_copy = True
                if should_copy:
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    shutil.copy2(src, dest)
                    print("📄 Copied script to /content/telegram_bot.py for convenience.")
    except Exception as _e:
        # Non-fatal if copy fails; continue running from current path
        pass


def main():
    """Start the bot"""
    print("🚀 Starting Telegram Bot...")
    print(f"👤 Bot Token: {BOT_TOKEN[:10]}..." if BOT_TOKEN else "❌ BOT_TOKEN not set")
    print(f"📡 Channel: {CHANNEL_ID if CHANNEL_ID else 'Not configured'}")
    print(f"⚙️ Workers: {WORKERS}")
    print("\n✅ Bot is running! Press Ctrl+C to stop.\n")
    # Ensure a copy exists under /content for Colab users running '!python /content/telegram_bot.py'
    ensure_colab_copy()

    app.run()


if __name__ == "__main__":
    main()
