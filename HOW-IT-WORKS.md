# LeadFlow AI - How It Actually Works

## What It Does

1. **Scans Reddit every day at 9 AM** (11 subreddits)
2. **Finds people who NEED web design/SEO** (not designers looking for work)
3. **Scores each lead A/B/C** (intent + budget + urgency signals)
4. **Generates a custom response for each lead** (you just copy/paste)
5. **Opens dashboard** showing all leads + ready-to-send replies

## Your Workflow

### Every Morning (5-10 minutes)

1. **Open dashboard** (auto-opens after scan, or run `dashboard.html`)
2. **Review top leads** (sorted by score, A-grade first)
3. **Copy the pre-written response** (click "Copy to Clipboard")
4. **Click "View on Reddit"** → paste your response → send
5. **Done.** Move to next lead.

### Example:

**Lead found:**
> "Hiring freelancers vs. agency for website redesign + SEO - what's been your experience?"
> 
> Budget: $25-40k | Timeline: 3-4 months | r/marketing

**Your response (pre-written):**
> Hey! Saw your post about hiring freelancers vs. agency.
> 
> I run UpGo Web AI Agency and we specialize in exactly this - modern web design + SEO that actually converts.
> 
> Quick wins we've delivered for similar clients:
> • 40% faster page speeds (better SEO + UX)  
> • Mobile-first designs  
> • SEO-optimized from day 1
> 
> No pressure, but if you want to chat about your project, I'd be happy to share what's worked for others in your space.
> 
> — Steve  
> UpGo Web AI Agency  
> https://upgo.ai

**You:** Copy → paste on Reddit → done in 30 seconds.

## What Makes This a "Lead"

**Not just anyone asking questions.** The system filters for:

✅ People who explicitly say "need help", "looking to hire", "want to hire"  
✅ Budget signals ($, price, pay, invest)  
✅ Urgency signals (ASAP, soon, this week)  
✅ Business owners / decision makers (not employees asking for advice)  

❌ Filters OUT designers, freelancers, developers looking for work  
❌ Filters OUT "just browsing" posts with no intent  

## Why Pre-Written Responses Work

1. **Speed** - You reply in 60 seconds vs 15 minutes writing from scratch
2. **Consistency** - Professional, helpful tone every time
3. **Proven** - Templates based on UpGo's $5k Reddit win
4. **Natural** - Doesn't sound like a sales pitch (genuine help)

## The Economics

**Manual prospecting:**
- 15+ hours/week scrolling Reddit
- Most leads are low-quality
- You reply too late (competitors got there first)
- Inconsistent messaging

**LeadFlow AI:**
- 5-10 minutes/day reviewing pre-filtered leads
- Only high-intent prospects
- Fast response (within hours of posting)
- Consistent, proven messaging

**ROI:** 1 client = $3k-10k project. You need 1 win to pay for a year of this tool.

## Files

- `dashboard.html` - Your daily dashboard (leads + responses)
- `leads.json` - All leads database
- `reddit_monitor.py` - The scanner
- `respond.py` - Response generator (runs automatically in dashboard)

## Manual Commands

```bash
# Run scan manually
python reddit_monitor.py

# Show responses in terminal
python respond.py

# Show specific lead response
python respond.py 2

# Open dashboard
start dashboard.html
```

## Schedule

**Automated:** Runs every day at 9 AM via Windows Task Scheduler  
**Task name:** `LeadFlowAI-Reddit-Monitor`

Change schedule:
1. Open Task Scheduler (search in Windows)
2. Find "LeadFlowAI-Reddit-Monitor"
3. Right-click → Properties → Triggers → Edit

---

**This is your product. Actually working. No bullshit.**

You wake up, check the dashboard, copy/paste 3-5 responses, and you're done prospecting for the day.
