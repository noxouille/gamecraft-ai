#!/usr/bin/env python3
"""Simple script to update IGDB token in .env file"""

import re
from pathlib import Path


def update_env_token(new_token: str):
    """Update the IGDB_ACCESS_TOKEN in .env file"""
    env_file = Path(".env")

    if not env_file.exists():
        print("❌ .env file not found")
        return False

    # Read current content
    content = env_file.read_text()

    # Replace the token
    new_content = re.sub(r"IGDB_ACCESS_TOKEN=.*", f"IGDB_ACCESS_TOKEN={new_token}", content)

    # Write back
    env_file.write_text(new_content)
    print(f"✅ Updated .env with new token: {new_token[:20]}...")
    return True


def main():
    print("🔧 IGDB Token Updater")
    print("=" * 50)

    print("Please generate your token manually:")
    print("1. Go to https://api.igdb.com/ and get your Client Secret")
    print("2. Run this curl command (replace YOUR_CLIENT_SECRET):")
    print()
    print("curl -X POST 'https://id.twitch.tv/oauth2/token' \\")
    print(
        "  -d 'client_id=704y68ri6xswd0ppq1s1k1wc1k50ty&client_secret=YOUR_CLIENT_SECRET&grant_type=client_credentials'"
    )
    print()

    token = input("🔑 Paste the generated access_token here: ").strip()

    if not token:
        print("❌ No token provided")
        return

    if update_env_token(token):
        print("✅ Token updated successfully!")
        print("🧪 Test it with: uv run python tests/test_apis.py")
    else:
        print("❌ Failed to update token")


if __name__ == "__main__":
    main()
