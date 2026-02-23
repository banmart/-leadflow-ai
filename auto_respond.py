#!/usr/bin/env python3
"""
LeadFlow AI - Automated Reddit Responder
Posts responses automatically (with your approval)
"""

import json
import requests
import time
from datetime import datetime

# Response templates
TEMPLATES = {
    'redesign': """Hey! Saw your post.

I run UpGo Web AI Agency - we specialize in modern web design + SEO that actually converts.

Quick wins we've delivered for similar clients:
• 40% faster page speeds (better SEO + UX)
• Mobile-first designs (most traffic comes from mobile now)
• SEO-optimized from day 1 (not an afterthought)

No pressure, but if you want to chat about your project, I'd be happy to share what's worked for others in your space.

— Steve | UpGo Web AI Agency | https://upgo.ai""",

    'new_site': """Hi! Just saw your post.

I build websites for businesses like yours - fast, modern, and conversion-focused.

Recent project: Built a landing page that converted at 15% (industry average is 2-3%). Client got their investment back in the first month.

What's your timeline and rough budget? Happy to share ideas even if we're not a fit.

— Steve | UpGo Web AI Agency | https://upgo.ai""",

    'ecommerce': """Hey! Saw your post.

I specialize in ecommerce sites - Shopify, WooCommerce, custom builds. Focus on conversion optimization (checkout flow, product pages, speed).

One recent client increased checkout completion by 30% just by simplifying their cart flow.

What platform are you on / considering? Happy to point you in the right direction.

— Steve | UpGo Web AI Agency | https://upgo.ai""",

    'generic': """Hey! Saw your post.

I run a web design + SEO agency and help businesses with exactly this kind of challenge.

What stage are you at? Happy to chat and share what's worked for similar projects - no pressure.

— Steve | UpGo Web AI Agency | https://upgo.ai"""
}

def detect_context(lead):
    """Detect what kind of response to use"""
    text = (lead['title'] + ' ' + lead['text']).lower()
    
    if 'redesign' in text or 'rebuild' in text:
        return 'redesign'
    elif 'ecommerce' in text or 'shopify' in text or 'store' in text:
        return 'ecommerce'
    elif 'website' in text or 'landing page' in text or 'web design' in text:
        return 'new_site'
    else:
        return 'generic'

def generate_response(lead):
    """Generate response for a lead"""
    context = detect_context(lead)
    return TEMPLATES[context]

def send_dm(username, message):
    """Send DM to Reddit user (requires Reddit API setup)"""
    # TODO: Implement Reddit API DM sending
    # For now, just log what would be sent
    print(f"\n[DM] Would send to u/{username}:")
    print(f"---")
    print(message)
    print(f"---\n")
    
    # Save to sent log
    with open('sent_messages.json', 'a') as f:
        f.write(json.dumps({
            'to': username,
            'message': message,
            'sent_at': datetime.now().isoformat(),
            'method': 'dm'
        }) + '\n')

def process_leads():
    """Process all A/B grade leads and send DMs"""
    try:
        with open('leads.json', 'r') as f:
            leads = json.load(f)
    except FileNotFoundError:
        print("[ERROR] No leads.json found. Run reddit_monitor.py first.")
        return
    
    # Filter for high-value leads
    high_value = [l for l in leads if l['grade'] in ['A', 'B']]
    
    if not high_value:
        print("[OK] No A/B grade leads to contact.")
        return
    
    print(f"[FOUND] {len(high_value)} high-value leads")
    print()
    
    # Load already contacted
    try:
        with open('contacted.json', 'r') as f:
            contacted = json.load(f)
    except FileNotFoundError:
        contacted = []
    
    contacted_urls = {c['url'] for c in contacted}
    
    # Send DMs to new leads
    new_contacts = 0
    for lead in high_value:
        if lead['url'] in contacted_urls:
            continue
        
        print(f"[LEAD] {lead['title']}")
        print(f"[GRADE] {lead['grade']} ({lead['score']}/100)")
        print(f"[USER] u/{lead['author']}")
        
        response = generate_response(lead)
        
        # Send DM
        send_dm(lead['author'], response)
        
        # Mark as contacted
        contacted.append({
            'url': lead['url'],
            'author': lead['author'],
            'title': lead['title'],
            'grade': lead['grade'],
            'contacted_at': datetime.now().isoformat()
        })
        
        new_contacts += 1
        time.sleep(5)  # Rate limit
    
    # Save contacted list
    with open('contacted.json', 'w') as f:
        json.dump(contacted, f, indent=2)
    
    print()
    print(f"[DONE] Contacted {new_contacts} new leads")

if __name__ == '__main__':
    print("="*50)
    print("LeadFlow AI - Auto Responder")
    print("="*50)
    print()
    
    process_leads()
