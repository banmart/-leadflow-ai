# LeadFlow AI - Simple Launch Plan

## What You're Selling

**Product:** Daily email digest of qualified web design leads  
**Price:** $149-499/mo (beta = 50% off lifetime)  
**Customer:** Web agencies & freelancers who need clients

## How It Works (Customer Side)

1. Customer signs up + pays via Stripe
2. Every morning, they get email with 3-10 leads
3. Leads = people on Reddit saying "I need a website" with budget signals
4. Customer contacts leads → closes deals → stays subscribed

## Your Setup (Next 30 Minutes)

### Step 1: Payment (5 min)

1. Go to https://stripe.com → Sign up
2. Create 3 payment links:
   - Starter: $149/mo recurring
   - Growth: $299/mo recurring
   - Agency: $499/mo recurring
3. Save the payment links

### Step 2: Signup Form (2 min)

1. Go to https://formspree.io → Sign up (free)
2. Create a form
3. Copy the form ID
4. Update `signup.html` line 106: Replace `YOUR_FORM_ID` with your Formspree ID
5. Deploy `signup.html` to Netlify

### Step 3: Email Setup (10 min)

1. Gmail → Settings → Security → 2-Step Verification → Enable
2. Then: App Passwords → Create app password → Copy it
3. Add to `.env`:
   ```
   SENDER_EMAIL=banmart@gmail.com
   SENDER_PASSWORD=<your app password>
   ```

### Step 4: First Customer (Manual Process)

**When someone signs up:**

1. You get email from Formspree with their details
2. Send them Stripe payment link for their chosen plan
3. After they pay, add them to `send_leads_email.py`:

```python
CUSTOMERS = [
    {
        'name': 'John Doe',
        'email': 'john@agency.com',
        'plan': 'growth',
        'leads_per_week': 50
    }
]
```

4. Run `python send_leads_email.py` to test
5. Set up daily automation (see below)

### Step 5: Automate Daily Emails (5 min)

**Windows Task Scheduler:**

```batch
schtasks /create /tn "LeadFlowAI-Daily-Email" /tr "python C:\Users\banma\.openclaw\workspace\projects\leadflow-ai\send_leads_email.py" /sc daily /st 08:00 /f
```

Now every morning at 8 AM, customers get their leads.

## Revenue Math

**First Week Goal: 3 Customers**

- 1 Starter ($149) + 2 Growth ($299) = **$747/mo**
- Annual value: **$8,964**
- They're locked in at 50% off forever

**First Month Goal: 10 Customers**

- Average: $250/mo × 10 = **$2,500/mo**
- Annual value: **$30,000**

**First Year Goal: 50 Customers**

- Average: $250/mo × 50 = **$12,500/mo**
- Annual value: **$150,000**

## Where to Find Customers

### Week 1 (Free Channels)

1. **Reddit** (r/webdev, r/freelance, r/web_design, r/Entrepreneur)
   - Post: "I built a tool that finds $25k+ web design leads on autopilot"
   - Include real screenshot of leads
   - Link to landing page

2. **Twitter** (when API works)
   - Tweet thread about how you found a $5k client in 48 hours
   - Explain the system
   - "Now available as SaaS"

3. **LinkedIn**
   - Post to your network
   - Tag web designers you know
   - Share case study

4. **Email 10 Agency Owners You Know**
   - Use template in `GO-TO-MARKET.md`
   - Offer first month free

### Week 2 (Paid Channels if needed)

- Facebook Ads targeting "web designer" interest ($5/day)
- Google Ads "lead generation for web designers"

## Handling Support

**First 10 customers = Manual**
- Answer emails personally
- Jump on Zoom calls
- Get feedback, improve product

**After 10 customers:**
- Create FAQ
- Consider Slack community (Agency tier)
- Hire VA for support ($10/hr)

## Next 48 Hours Checklist

- [ ] Set up Stripe payment links
- [ ] Set up Formspree signup form
- [ ] Update `signup.html` with Formspree ID
- [ ] Deploy updated `index.html` + `signup.html` to Netlify
- [ ] Set up Gmail app password
- [ ] Test email delivery to yourself
- [ ] Post on Reddit announcing beta launch
- [ ] Email 5 warm contacts
- [ ] Get first customer 🎉

---

**You don't need perfect software. You need 1 paying customer.**

Get the first one manually, then automate as you grow.
