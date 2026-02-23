# LeadFlow AI - Full Twitter Automation

## 🚀 What This Does

**100% automated Twitter marketing for @leadsflowbot:**
- Posts launch thread
- Schedules Week 1 content (3 tweets/day)
- Auto-posts from queue every hour
- Monitors mentions (you can reply via BangBot)
- Tracks engagement

**Zero manual work after 5-minute setup.**

## ⚡ Quick Start (5 Minutes)

### 1. Get Twitter API Access
```bash
# Open in browser:
https://developer.twitter.com/en/portal/dashboard

# Follow guide:
TWITTER-API-SETUP.md
```

### 2. Add Credentials
```bash
# Copy template:
copy .env.example .env

# Edit .env and paste your 5 API keys from Twitter
notepad .env
```

### 3. Launch Everything
```bash
# Post launch thread + schedule Week 1:
python launch_campaign.py all

# Set up hourly auto-posting:
setup_twitter_automation.bat
```

## ✅ Done!

Twitter now runs itself:
- Launch thread: Posted
- Week 1 content: Scheduled (3x daily)
- Auto-posting: Every hour via Task Scheduler
- Monitoring: BangBot handles mentions

## 📋 Commands

### Post Now
```bash
python twitter_bot.py post "Your tweet text here"
```

### Post Thread
```bash
python twitter_bot.py thread "Tweet 1" "Tweet 2" "Tweet 3"
```

### Check Mentions
```bash
python twitter_bot.py mentions
```

### Show Scheduled Posts
```bash
python launch_campaign.py show
```

### Process Queue Manually
```bash
python twitter_bot.py queue
```

## 🎯 Week 1 Schedule

**Day 1:** Launch thread (6 tweets)
**Day 2-7:** 3 posts/day (tips, engagement, updates)

**Total:** 19 automated posts in Week 1

Mix of:
- Lead gen tips (5)
- Engagement posts (4)
- Customer success (2)
- Product updates (2)
- Campaign updates (3)

## 🔧 Customization

**Edit content:** `launch_content.json`
**Edit schedule:** `launch_campaign.py` (schedule_week_1 function)
**Add more posts:** Append to `twitter_queue.json`

## 🤖 BangBot Integration

BangBot can:
1. Draft new tweets for you
2. Reply to mentions
3. Monitor engagement
4. Adjust strategy based on performance

**Just ask:** "BangBot, draft 3 tweets about [topic]"

## 📊 Monitoring

Check analytics:
- Twitter Analytics: https://analytics.twitter.com
- Scheduled posts: `python launch_campaign.py show`
- Posted tweets: Check @leadsflowbot timeline

## 🚨 Troubleshooting

**"Invalid credentials"**
- Regenerate tokens in Twitter Developer Portal
- Update `.env` file

**"Read-only mode"**
- Enable Read & Write permissions in app settings
- Regenerate access token after permission change

**"Rate limit exceeded"**
- Twitter limits: 50 posts/day (Free tier)
- Wait 15 minutes and try again

**Scheduled task not running**
- Run `setup_twitter_automation.bat` as Administrator
- Check Task Scheduler: Search "Task Scheduler" in Windows

## 🎓 Best Practices

1. **Never spam** - Quality > quantity
2. **Engage genuinely** - Reply to comments
3. **Track what works** - A/B test content
4. **Post consistently** - 3x daily optimal
5. **Mix content types** - Tips, questions, updates

## 🔐 Security

- **Never commit `.env` file** (in .gitignore)
- **Keep API keys private**
- **Regenerate tokens if exposed**

## 📈 Growth Hacks

1. **Reply to big accounts** - Piggyback on engagement
2. **Use polls** - 2x more engagement
3. **Tag customers** - Social proof
4. **Quote tweet wins** - Showcase success
5. **Morning posts** - 9-11 AM best time

---

**Questions?** Ask BangBot or email mybangbot@gmail.com
