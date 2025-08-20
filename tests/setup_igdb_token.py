#!/usr/bin/env python3
"""Script to generate IGDB App Access Token"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx  # noqa: E402

from src.gamecraft_ai.config import settings  # noqa: E402


def generate_igdb_access_token(client_id: str, client_secret: str) -> str | None:
    """Generate IGDB App Access Token using Client ID and Client Secret"""
    try:
        # IGDB uses Twitch OAuth for authentication
        url = "https://id.twitch.tv/oauth2/token"

        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }

        response = httpx.post(url, data=data)
        response.raise_for_status()

        token_data = response.json()
        return token_data.get("access_token")

    except Exception as e:
        print(f"Error generating access token: {e}")
        return None


def test_igdb_token(client_id: str, access_token: str) -> bool:
    """Test if the IGDB access token works"""
    try:
        headers = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        query = "fields name; limit 1;"
        response = httpx.post("https://api.igdb.com/v4/games", headers=headers, content=query)
        response.raise_for_status()

        data = response.json()
        return len(data) > 0

    except Exception as e:
        print(f"Error testing token: {e}")
        return False


def main():
    print("🎮 IGDB Access Token Generator")
    print("=" * 50)

    client_id = settings.igdb_client_id
    if not client_id or client_id == "your_igdb_client_id_here":
        print("❌ IGDB Client ID not found in .env file")
        print("Please add IGDB_CLIENT_ID to your .env file")
        return

    print(f"✅ Client ID found: {client_id}")

    # You need to provide the client secret (not stored in .env for security)
    client_secret = input("🔑 Enter your IGDB Client Secret: ").strip()

    if not client_secret:
        print("❌ Client Secret is required")
        return

    print("\n🔄 Generating access token...")
    access_token = generate_igdb_access_token(client_id, client_secret)

    if not access_token:
        print("❌ Failed to generate access token")
        print("Please check your Client ID and Client Secret")
        return

    print(f"✅ Access token generated: {access_token[:20]}...")

    print("\n🧪 Testing access token...")
    if test_igdb_token(client_id, access_token):
        print("✅ Access token works!")
        print("\n📝 Update your .env file with:")
        print(f"IGDB_ACCESS_TOKEN={access_token}")
    else:
        print("❌ Access token test failed")

    print("\n💡 Remember: Access tokens expire, so you may need to regenerate them periodically.")


if __name__ == "__main__":
    main()
