#!/usr/bin/env python3
"""
LeadFlow AI - Response Generator
Generates custom replies for each lead that you can copy/paste
"""

import json
import sys

# Response templates based on context
TEMPLATES = {
    'redesign': """Hey! Saw your post about {topic}.

I run UpGo Web AI Agency and we specialize in exactly this - modern web design + SEO that actually converts.

Quick wins we've delivered for similar clients:
• 40% faster page speeds (better SEO + UX)
• Mobile-first designs (most traffic comes from mobile now)
• SEO-optimized from day 1 (not an afterthought)

No pressure, but if you want to chat about your project, I'd be happy to share what's worked for others in your space.

— Steve
UpGo Web AI Agency
https://upgo.ai""",

    'new_site': """Hi! Just saw your post about {topic}.

I build websites for businesses like yours - fast, modern, and conversion-focused.

Recent project: Built a landing page that converted at 15% (industry average is 2-3%). Client got their investment back in the first month.

What's your timeline and rough budget? Happy to share ideas even if we're not a fit.

— Steve
UpGo Web AI Agency
https://upgo.ai""",

    'ecommerce': """Hey! Saw you're working on {topic}.

I specialize in ecommerce sites - Shopify, WooCommerce, custom builds. Focus on conversion optimization (checkout flow, product pages, speed).

One recent client increased checkout completion by 30% just by simplifying their cart flow.

What platform are you on / considering? Happy to point you in the right direction.

— Steve
UpGo Web AI Agency
https://upgo.ai""",

    'seo': """Hi! Read your post about {topic}.

I do technical SEO + content strategy for web agencies and small businesses.

Recent win: Got a client from page 3 to page 1 for their main keyword in 6 weeks (15x more organic traffic).

What's your current SEO situation? Happy to do a quick audit and share what I'd prioritize.

— Steve
UpGo Web AI Agency
https://upgo.ai""",

    'generic': """Hey! Saw your post about {topic}.

I run a web design + SEO agency and help businesses with exactly this kind of challenge.

What stage are you at? Happy to chat and share what's worked for similar projects - no pressure.

— Steve
UpGo Web AI Agency
https://upgo.ai"""
}

def detect_context(lead):
    """Detect what kind of response to use"""
    text = (lead['title'] + ' ' + lead['text']).lower()
    
    if 'redesign' in text or 'rebuild' in text:
        return 'redesign'
    elif 'ecommerce' in text or 'shopify' in text or 'store' in text:
        return 'ecommerce'
    elif 'seo' in text or 'ranking' in text or 'traffic' in text:
        return 'seo'
    elif 'website' in text or 'landing page' in text or 'web design' in text:
        return 'new_site'
    else:
        return 'generic'

def generate_response(lead):
    """Generate a custom response for a lead"""
    context = detect_context(lead)
    template = TEMPLATES[context]
    
    # Extract topic from title
    topic = lead['title'].lower().replace('[', '').replace(']', '')
    
    # Generate response
    response = template.format(topic=topic)
    
    return {
        'lead': lead,
        'response': response,
        'context': context,
        'reddit_url': lead['url']
    }

def show_lead_with_response(lead):
    """Display lead + ready-to-send response"""
    resp = generate_response(lead)
    
    print("\n" + "="*70)
    print(f"LEAD: {lead['title']}")
    print(f"Grade: {lead['grade']} ({lead['score']}/100)")
    print(f"Subreddit: r/{lead['subreddit']}")
    print(f"URL: {lead['url']}")
    print("="*70)
    print("\nORIGINAL POST:")
    print(lead['text'][:300] + "..." if len(lead['text']) > 300 else lead['text'])
    print("\n" + "-"*70)
    print("YOUR RESPONSE (copy/paste this):")
    print("-"*70)
    print(resp['response'])
    print("-"*70)
    print()

def process_all_leads():
    """Show all leads with responses"""
    try:
        with open('leads.json', 'r') as f:
            leads = json.load(f)
    except FileNotFoundError:
        print("No leads found. Run reddit_monitor.py first.")
        return
    
    if not leads:
        print("No leads yet.")
        return
    
    # Sort by score
    leads.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\nFound {len(leads)} leads. Showing responses for top leads:\n")
    
    # Show top 5 with responses
    for i, lead in enumerate(leads[:5], 1):
        print(f"\n{'='*70}")
        print(f"LEAD #{i} - Grade {lead['grade']} ({lead['score']}/100)")
        show_lead_with_response(lead)
        
        if i < 5:
            input("Press Enter for next lead...")

def process_single_lead(lead_num):
    """Show single lead with response"""
    try:
        with open('leads.json', 'r') as f:
            leads = json.load(f)
    except FileNotFoundError:
        print("No leads found. Run reddit_monitor.py first.")
        return
    
    leads.sort(key=lambda x: x['score'], reverse=True)
    
    if lead_num > len(leads):
        print(f"Only {len(leads)} leads available.")
        return
    
    lead = leads[lead_num - 1]
    show_lead_with_response(lead)

if __name__ == '__main__':
    print("="*70)
    print("LeadFlow AI - Response Generator")
    print("="*70)
    
    if len(sys.argv) > 1:
        # Show specific lead
        try:
            lead_num = int(sys.argv[1])
            process_single_lead(lead_num)
        except ValueError:
            print("Usage: python respond.py [lead_number]")
    else:
        # Show all leads
        process_all_leads()
