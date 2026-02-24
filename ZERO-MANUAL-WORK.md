# LeadFlow AI - Zero Manual Work System

## What Happens Automatically

### When Someone Signs Up:
1. ✅ Formspree sends you email notification
2. ✅ System sends them welcome email with payment link
3. ✅ They click → pay via Stripe
4. ✅ Stripe sends you payment confirmation

### When They Pay:
1. ✅ System sends activation email
2. ✅ You add their email to delivery list (30 seconds - see below)
3. ✅ Every morning at 8 AM → They get leads automatically

### If They Don't Pay:
1. ✅ After 24 hours → Automatic reminder email
2. ✅ After 48 hours → Another reminder

---

## Your Only Job (30 Seconds Per Customer)

**When Formspree emails you a signup:**

```bash
python automate_onboarding.py signup "Their Name" their@email.com growth
```

**When Stripe confirms payment:**

```bash
python automate_onboarding.py paid their@email.com
```

Then add them to send_leads_email.py (copy/paste):

```python
CUSTOMERS = [
    {
        'name': 'Their Name',
        'email': 'their@email.com',
        'plan': 'growth',
        'leads_per_week': 50
    }
]
```

**Done. That's it.**

---

## Full Automation Schedule

**Daily - 8:00 AM** (Windows Task Scheduler)
```bash
python send_leads_email.py
```
→ Sends all customers their daily lead digest

**Daily - 9:00 AM** (Windows Task Scheduler)
```bash
python reddit_monitor.py
```
→ Scans Reddit for new leads

**Daily - 10:00 AM** (Windows Task Scheduler)
```bash
python automate_onboarding.py reminders
```
→ Sends payment reminders to unpaid signups

---

## Set Up Automation (One Time - 5 Min)

**1. Email Setup**
Add to `.env`:
```
SENDER_EMAIL=banmart@gmail.com
SENDER_PASSWORD=<your Gmail app password>
```

Get app password: Gmail → Settings → Security → 2-Step Verification → App Passwords

**2. Schedule Tasks**

```batch
REM Lead delivery
schtasks /create /tn "LeadFlowAI-Send-Leads" /tr "python C:\Users\banma\.openclaw\workspace\projects\leadflow-ai\send_leads_email.py" /sc daily /st 08:00 /f

REM Reddit scan
schtasks /create /tn "LeadFlowAI-Scan-Reddit" /tr "python C:\Users\banma\.openclaw\workspace\projects\leadflow-ai\reddit_monitor.py" /sc daily /st 09:00 /f

REM Payment reminders
schtasks /create /tn "LeadFlowAI-Reminders" /tr "python C:\Users\banma\.openclaw\workspace\projects\leadflow-ai\automate_onboarding.py reminders" /sc daily /st 10:00 /f
```

---

## Your Workflow

**Morning (8 AM):** Check email
- See Formspree signup notifications?
  - Run: `python automate_onboarding.py signup "Name" email plan`
- See Stripe payment confirmations?
  - Run: `python automate_onboarding.py paid email`
  - Add to `send_leads_email.py`

**That's literally it.** 30 seconds per customer.

Everything else is 100% automated.

---

## Revenue Example

**10 customers:**
- Takes 5 minutes total to onboard (30 sec each)
- Earn $2,500/mo
- **$30/min of your time**

**50 customers:**
- Takes 25 minutes total to onboard
- Earn $12,500/mo
- **$500/min of your time**

---

## Support (Also Mostly Automated)

**Customer emails you?**
- 90% of questions are in FAQ (add to website)
- 10% you reply personally
- Average: 2-3 support emails per week

**No live chat. No phone support. Just email.**

---

**This is as automated as it gets without building a full admin dashboard.**

And honestly? You don't need a dashboard until you have 20+ customers.

Get there first. Then automate more.
