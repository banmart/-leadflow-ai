# LeadFlow AI - Working Reddit Monitor

## ✅ What's Done

**Reddit lead generation is RUNNING:**

- Scans 10 subreddits: web_design, webdev, freelance, forhire, Entrepreneur, smallbusiness, startups, SaaS, ecommerce, SEO
- Scores leads 0-100 (A/B/C grades)
- Saves to `leads.json`
- Generates HTML report: `leads-report.html`
- **Automated**: Runs every day at 9 AM

## 📊 First Run Results

**56 leads found**

Top 3:
1. **Grade A (80/100)** - VA's for agency hiring
2. **Grade A (75/100)** - Freelancer lost clients due to inactive Instagram
3. **Grade A (75/100)** - Person willing to work for $15-20

## 🚀 How to Use

### View Latest Leads
```bash
# Open the HTML report:
start C:\Users\banma\.openclaw\workspace\projects\leadflow-ai\leads-report.html
```

### Run Manually
```bash
cd C:\Users\banma\.openclaw\workspace\projects\leadflow-ai
python reddit_monitor.py
```

### Automated Schedule
**Already set up!** Runs daily at 9 AM via Windows Task Scheduler

Task name: `LeadFlowAI-Reddit-Monitor`

To change schedule:
- Open Task Scheduler (search in Windows)
- Find "LeadFlowAI-Reddit-Monitor"
- Right-click → Properties → Triggers

## 📁 Files

- `leads.json` - All leads (newest first)
- `leads-report.html` - Visual report (top 50)
- `reddit_monitor.py` - The scanner
- `run_monitor.bat` - Quick run script

## 🎯 Lead Scoring

**Grade A (70-100):** High intent + budget signals + urgency
**Grade B (50-69):** Some intent, worth checking
**Grade C (40-49):** Low priority

## Next Steps

1. Check `leads-report.html` daily
2. Reply to A-grade leads first
3. Customize keywords in `reddit_monitor.py` if needed
4. Track which subreddits convert best

---

**This is the actual product. Working. No bullshit.**
