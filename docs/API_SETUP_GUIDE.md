# API Setup Guide

This guide will help you set up the required API keys for GameCraft AI to work properly.

## 🎮 IGDB API Setup (Game Database)

### 1. Create IGDB Account
1. Go to [IGDB API](https://api.igdb.com/)
2. Click "Get Started" and sign up/login with Twitch
3. Create a new application
4. Note your **Client ID** and **Client Secret**

### 2. Generate Access Token
The IGDB API requires a dynamic access token (not just Client ID/Secret).

**Option A: Use our setup script**
```bash
uv run python tests/setup_igdb_token.py
```
Enter your Client Secret when prompted, and it will generate the access token for you.

**Option B: Manual generation**
```bash
curl -X POST 'https://id.twitch.tv/oauth2/token' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&grant_type=client_credentials'
```

### 3. Update .env file
```bash
IGDB_CLIENT_ID=your_actual_client_id
IGDB_ACCESS_TOKEN=your_generated_access_token
```

---

## 📺 YouTube Data API Setup

### 1. Enable YouTube Data API v3
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Navigate to **APIs & Services** > **Library**
4. Search for "YouTube Data API v3"
5. Click on it and press **ENABLE**

### 2. Create API Key
1. Go to **APIs & Services** > **Credentials**
2. Click **+ CREATE CREDENTIALS** > **API Key**
3. Copy the generated API key
4. (Optional) Restrict the key to YouTube Data API v3 for security

### 3. Update .env file
```bash
YOUTUBE_API_KEY=your_actual_youtube_api_key
```

---

## 🤖 OpenAI API Setup (Already Working)

Your OpenAI API key appears to be working correctly. If you need a new one:

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Update .env:
```bash
OPENAI_API_KEY=your_openai_api_key
```

---

## 🧪 Testing Your Setup

After configuring the APIs, test them:

```bash
# Test all APIs
uv run python tests/test_apis.py

# Test specific API
uv run python -c "from src.gamecraft_ai.services.igdb import IGDBService; print(IGDBService().search_game('Zelda'))"
```

---

## 🔧 Troubleshooting

### IGDB Issues
- **401 Unauthorized**: Access token expired or invalid → Regenerate using setup script
- **403 Forbidden**: Client ID/Secret incorrect → Check credentials

### YouTube Issues
- **403 Forbidden**: API not enabled → Enable YouTube Data API v3 in Google Cloud Console
- **400 Bad Request**: Invalid parameters → Check API key format
- **429 Too Many Requests**: Quota exceeded → Wait or increase quota

### Common Solutions
1. **Check .env file**: Ensure no extra spaces or quotes around API keys
2. **Restart application**: After updating .env, restart the application
3. **Check quotas**: Most APIs have usage limits
4. **Network issues**: Try from different network if corporate firewall blocks APIs

---

## 📝 Quick Fix Commands

```bash
# Regenerate IGDB token
uv run python tests/setup_igdb_token.py

# Test APIs after setup
uv run python tests/test_apis.py

# Test full workflow
uv run python -c "
from src.gamecraft_ai.graph.workflow import WorkflowManager
wm = WorkflowManager()
result = wm.process_query('Create a review for Zelda', 10)
print('Success:', result['success'])
"
```

Once all APIs are properly configured, the workflow should work without fallback data! 🚀
