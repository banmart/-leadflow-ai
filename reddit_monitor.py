#!/usr/bin/env python3
"""
LeadFlow AI - Reddit Lead Monitor
Finds CLIENTS who need web design/dev work (not designers looking for work)
"""

import requests
import json
import time
from datetime import datetime
import re

# Subreddits where clients post
SUBREDDITS = [
    'Entrepreneur', 'smallbusiness', 'startups', 'SaaS', 
    'ecommerce', 'shopify', 'marketing', 'SEO',
    'web_design', 'webdev', 'digitalnomad'
]

# CLIENT signals (people who NEED help)
CLIENT_KEYWORDS = {
    'need': ['need a website', 'need a web', 'need help with', 'looking for a web', 'looking for someone', 'want to hire', 'looking to hire', 'need someone to'],
    'budget': ['budget of', 'willing to pay', 'can pay', 'budget is', '$', 'price range'],
    'urgency': ['asap', 'urgent', 'quickly', 'this week', 'immediately', 'soon', 'by next'],
    'project': ['website', 'web design', 'web app', 'landing page', 'ecommerce site', 'shopify store', 'redesign', 'wordpress']
}

# FILTER OUT designer/freelancer posts (we don't want these)
EXCLUDE_KEYWORDS = [
    'i am a', 'i\'m a web', 'freelance web', 'for hire', '[for hire]', 
    'offering my services', 'portfolio', 'my work', 'available for',
    'looking for work', 'looking for clients', 'need clients'
]

def is_client_post(post):
    """Check if post is from a CLIENT (not a designer)"""
    text = (post['title'] + ' ' + post.get('selftext', '')).lower()
    
    # Exclude designer/freelancer posts
    for keyword in EXCLUDE_KEYWORDS:
        if keyword in text:
            return False
    
    return True

def score_lead(post):
    """Score lead 0-100 based on client intent signals"""
    if not is_client_post(post):
        return 0
    
    score = 0
    text = (post['title'] + ' ' + post.get('selftext', '')).lower()
    
    # Need/looking signals (+40)
    need_count = sum(1 for kw in CLIENT_KEYWORDS['need'] if kw in text)
    score += min(need_count * 20, 40)
    
    # Budget signals (+30)
    budget_count = sum(1 for kw in CLIENT_KEYWORDS['budget'] if kw in text)
    score += min(budget_count * 15, 30)
    
    # Urgency signals (+15)
    urgency_count = sum(1 for kw in CLIENT_KEYWORDS['urgency'] if kw in text)
    score += min(urgency_count * 10, 15)
    
    # Project type match (+15)
    project_count = sum(1 for kw in CLIENT_KEYWORDS['project'] if kw in text)
    score += min(project_count * 5, 15)
    
    return min(score, 100)

def grade_lead(score):
    """Convert score to letter grade"""
    if score >= 70:
        return 'A'
    elif score >= 50:
        return 'B'
    elif score >= 30:
        return 'C'
    else:
        return 'D'

def scan_subreddit(subreddit, limit=50):
    """Scan subreddit for client posts"""
    url = f'https://www.reddit.com/r/{subreddit}/new.json?limit={limit}'
    headers = {'User-Agent': 'LeadFlowAI/1.0'}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return []
        
        data = resp.json()
        posts = data['data']['children']
        
        leads = []
        for post in posts:
            p = post['data']
            score = score_lead(p)
            
            if score >= 30:  # Only save actual client leads
                leads.append({
                    'title': p['title'],
                    'text': p.get('selftext', '')[:500],
                    'url': f"https://reddit.com{p['permalink']}",
                    'subreddit': subreddit,
                    'author': p['author'],
                    'created': datetime.fromtimestamp(p['created_utc']).isoformat(),
                    'score': score,
                    'grade': grade_lead(score)
                })
        
        return leads
    
    except Exception as e:
        print(f"[ERROR] {subreddit}: {e}")
        return []

def save_leads(leads, filename='leads.json'):
    """Save leads to JSON file"""
    try:
        # Load existing
        try:
            with open(filename, 'r') as f:
                existing = json.load(f)
        except FileNotFoundError:
            existing = []
        
        # Add new (avoid duplicates)
        existing_urls = {lead['url'] for lead in existing}
        new_leads = [lead for lead in leads if lead['url'] not in existing_urls]
        
        if new_leads:
            all_leads = existing + new_leads
            # Sort by score
            all_leads.sort(key=lambda x: x['score'], reverse=True)
            
            with open(filename, 'w') as f:
                json.dump(all_leads, f, indent=2)
            
            print(f"[SAVED] {len(new_leads)} new leads")
            return new_leads
        else:
            print("[OK] No new leads")
            return []
    
    except Exception as e:
        print(f"[ERROR] Save failed: {e}")
        return []

def generate_report(leads):
    """Generate HTML report of CLIENT leads"""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>LeadFlow AI - Client Leads</title>
    <style>
        body { font-family: system-ui; max-width: 1200px; margin: 40px auto; padding: 0 20px; background: #f9fafb; }
        h1 { color: #2563eb; }
        .stats { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; display: flex; gap: 40px; }
        .stat { flex: 1; }
        .stat-value { font-size: 32px; font-weight: bold; color: #2563eb; }
        .stat-label { color: #6b7280; font-size: 14px; }
        .lead { background: white; border: 1px solid #e5e7eb; padding: 20px; margin: 20px 0; border-radius: 8px; }
        .grade-A { border-left: 4px solid #10b981; }
        .grade-B { border-left: 4px solid #f59e0b; }
        .grade-C { border-left: 4px solid #6b7280; }
        .meta { color: #6b7280; font-size: 14px; margin: 10px 0; }
        .score { font-weight: bold; font-size: 18px; }
        .grade-A .score { color: #10b981; }
        .grade-B .score { color: #f59e0b; }
        .grade-C .score { color: #6b7280; }
        a { color: #2563eb; text-decoration: none; font-weight: 500; }
        a:hover { text-decoration: underline; }
        .title { font-size: 18px; margin: 10px 0; color: #111827; }
    </style>
</head>
<body>
    <h1>🚀 LeadFlow AI - Client Leads</h1>
    <p>Generated: """ + datetime.now().strftime('%Y-%m-%d %I:%M %p') + """</p>
    
    <div class="stats">
        <div class="stat">
            <div class="stat-value">""" + str(len([l for l in leads if l['grade'] == 'A'])) + """</div>
            <div class="stat-label">A-Grade Leads</div>
        </div>
        <div class="stat">
            <div class="stat-value">""" + str(len([l for l in leads if l['grade'] == 'B'])) + """</div>
            <div class="stat-label">B-Grade Leads</div>
        </div>
        <div class="stat">
            <div class="stat-value">""" + str(len(leads)) + """</div>
            <div class="stat-label">Total Leads</div>
        </div>
    </div>
"""
    
    for lead in leads:
        html += f"""
    <div class="lead grade-{lead['grade']}">
        <div class="score">Grade {lead['grade']} ({lead['score']}/100)</div>
        <div class="title">{lead['title']}</div>
        <p>{lead['text'][:300]}{'...' if len(lead['text']) > 300 else ''}</p>
        <div class="meta">
            r/{lead['subreddit']} • u/{lead['author']} • {lead['created']}
        </div>
        <a href="{lead['url']}" target="_blank">View on Reddit →</a>
    </div>
"""
    
    html += """
</body>
</html>
"""
    
    with open('leads-report.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[REPORT] leads-report.html")

if __name__ == '__main__':
    print("="*50)
    print("LeadFlow AI - Client Lead Monitor")
    print("Finding people who NEED web design")
    print("="*50)
    print()
    
    all_leads = []
    
    for sub in SUBREDDITS:
        print(f"[SCANNING] r/{sub}...")
        leads = scan_subreddit(sub)
        if leads:
            print(f"[FOUND] {len(leads)} client leads")
            all_leads.extend(leads)
        time.sleep(2)  # Rate limit
    
    print()
    print(f"[TOTAL] {len(all_leads)} client leads found")
    
    if all_leads:
        new_leads = save_leads(all_leads)
        all_leads.sort(key=lambda x: x['score'], reverse=True)
        generate_report(all_leads[:50])  # Top 50
        
        print()
        print("Top 5 Leads:")
        for i, lead in enumerate(all_leads[:5], 1):
            print(f"\n{i}. [{lead['grade']} - {lead['score']}/100] {lead['title']}")
            print(f"   r/{lead['subreddit']}")
            print(f"   {lead['url']}")
    else:
        print("\n[INFO] No client leads found this scan. Try again later.")
