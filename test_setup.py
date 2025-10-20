"""
Test script to verify bot setup
Run this in Colab to check if everything is configured correctly
"""

import os
import sys

def check_environment():
    """Check if all environment variables are set"""
    print("🔍 Checking environment variables...\n")
    
    required_vars = {
        "API_ID": os.environ.get("API_ID"),
        "API_HASH": os.environ.get("API_HASH"),
        "BOT_TOKEN": os.environ.get("BOT_TOKEN")
    }
    
    optional_vars = {
        "CHANNEL_ID": os.environ.get("CHANNEL_ID")
    }
    
    all_good = True
    
    for var_name, var_value in required_vars.items():
        if not var_value or var_value.startswith("your_"):
            print(f"❌ {var_name}: Not set or using default value")
            all_good = False
        else:
            masked_value = var_value[:10] + "..." if len(var_value) > 10 else var_value
            print(f"✅ {var_name}: {masked_value}")
    
    for var_name, var_value in optional_vars.items():
        if not var_value or var_value.startswith("@your_"):
            print(f"⚠️  {var_name}: Not set (optional)")
        else:
            print(f"✅ {var_name}: {var_value}")
    
    return all_good

def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...\n")
    
    try:
        import pyrogram
        print(f"✅ Pyrogram: {pyrogram.__version__}")
    except ImportError:
        print("❌ Pyrogram: Not installed")
        print("   Run: pip install pyrogram")
        return False
    
    try:
        import tgcrypto
        print(f"✅ TgCrypto: {tgcrypto.__version__}")
        print("   🚀 Speed boost enabled!")
    except ImportError:
        print("⚠️  TgCrypto: Not installed (optional but recommended)")
        print("   Run: pip install TgCrypto")
        print("   This provides 10-20x speed improvement!")
    
    return True

def check_files():
    """Check if bot files exist"""
    print("\n🔍 Checking files...\n")
    
    files = ["telegram_bot.py", "requirements.txt"]
    all_exist = True
    
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file}: {size} bytes")
        else:
            print(f"❌ {file}: Not found")
            all_exist = False
    
    return all_exist

def test_connection():
    """Test Telegram connection"""
    print("\n🔍 Testing Telegram connection...\n")
    
    try:
        from pyrogram import Client
        
        api_id = os.environ.get("API_ID")
        api_hash = os.environ.get("API_HASH")
        bot_token = os.environ.get("BOT_TOKEN")
        
        if not all([api_id, api_hash, bot_token]):
            print("❌ Cannot test connection: credentials not set")
            return False
        
        print("⏳ Connecting to Telegram...")
        
        app = Client(
            "test_session",
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token
        )
        
        with app:
            bot = app.get_me()
            print(f"✅ Connected successfully!")
            print(f"   Bot Name: {bot.first_name}")
            print(f"   Bot Username: @{bot.username}")
            print(f"   Bot ID: {bot.id}")
        
        # Clean up test session
        if os.path.exists("test_session.session"):
            os.remove("test_session.session")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("🤖 TELEGRAM BOT SETUP VERIFICATION")
    print("=" * 60)
    
    env_ok = check_environment()
    deps_ok = check_dependencies()
    files_ok = check_files()
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    if env_ok and deps_ok and files_ok:
        print("\n✅ All basic checks passed!")
        
        # Test connection
        conn_ok = test_connection()
        
        if conn_ok:
            print("\n" + "=" * 60)
            print("🎉 SETUP COMPLETE!")
            print("=" * 60)
            print("\n✨ Your bot is ready to use!")
            print("\n📝 Next steps:")
            print("   1. Run: python telegram_bot.py")
            print("   2. Open Telegram and search for your bot")
            print("   3. Send /start command")
            print("   4. Send a video to test!")
        else:
            print("\n⚠️  Setup incomplete - fix connection issues above")
    else:
        print("\n❌ Setup incomplete - fix the issues above")
        print("\n📝 Quick fixes:")
        if not env_ok:
            print("   - Set environment variables correctly")
        if not deps_ok:
            print("   - Run: pip install -r requirements.txt")
        if not files_ok:
            print("   - Make sure all files are uploaded")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
