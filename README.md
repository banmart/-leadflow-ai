# LeadFlow AI - Automated Lead Generation

## What It Does

Monitors Reddit 24/7, finds clients who need web design/SEO, sends them DMs automatically.

**Zero manual work.**

## Setup

1. Run monitor once to test:
```bash
python reddit_monitor.py
```

2. Check results:
```bash
type leads.json
```

3. Automated daily scan already set up (9 AM via Task Scheduler)

## Files

- `reddit_monitor.py` - Scans Reddit for client leads
- `auto_respond.py` - Sends automated DMs (requires Reddit API)
- `leads.json` - All leads found
- `contacted.json` - Tracking sent messages

## Status

✅ Reddit monitoring: Working  
⏳ Auto-DM: Needs Reddit API credentials  

---

**This is your SaaS product. The code customers pay for.**
