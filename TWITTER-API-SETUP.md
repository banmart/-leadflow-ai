# Twitter API Setup - 5 Minute Guide

## Why You Need This (Once)

Twitter API gives BangBot full control to post, reply, and monitor @leadsflowbot automatically. One-time setup = forever automated.

## Step-by-Step

### 1. Apply for Twitter Developer Account (2 min)
1. Go to: https://developer.twitter.com/en/portal/dashboard
2. Sign in with @leadsflowbot account
3. Click "Apply for a developer account"
4. Select "Hobbyist" → "Making a bot"
5. Describe: "Automated Twitter account for LeadFlow AI SaaS product - posts product updates, customer success stories, and industry tips"
6. Accept terms
7. **Instant approval** (usually immediate for basic access)

### 2. Create App & Get Credentials (3 min)
1. Dashboard → Projects & Apps → Create App
2. App name: `leadflowbot-automation`
3. Copy all 5 credentials to `.env` file:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret
   - Bearer Token

### 3. Enable Permissions
1. App Settings → User authentication settings → Edit
2. Enable: **Read and Write**
3. Type of App: **Web App**
4. Callback URL: `https://leadsflowbot.com`
5. Website: `https://leadsflowbot.com`
6. Save

### 4. Test It
```bash
cd C:\Users\banma\.openclaw\workspace\projects\leadflow-ai
python twitter_bot.py post "🚀 Testing automation - if you see this, BangBot is live!"
```

## Done! 

Now BangBot can:
- Post tweets on command
- Schedule content
- Reply to mentions
- Monitor engagement
- Run campaigns

**No more manual posting. Ever.**

## Common Issues

**"App suspended"** - Wait 5 min, Twitter auto-reviews and approves
**"Read-only"** - Go back to permissions, enable Write access
**"Invalid credentials"** - Regenerate tokens in developer portal

---

**After setup, delete this file or keep for reference.**
