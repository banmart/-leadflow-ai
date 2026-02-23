#!/usr/bin/env python3
"""
LeadFlow AI - Core Lead Generation Engine
Monitors Reddit, LinkedIn, Twitter for high-intent prospects
"""

import os
import json
import requests
import re
from datetime import datetime, timedelta
from typing import List, Dict
import time

class LeadEngine:
    """AI-powered lead generation engine"""
    
    def __init__(self):
        self.platforms = {
            'reddit': True,
            'linkedin': False,  # Coming soon
            'twitter': False    # Coming soon
        }
        self.leads_found = []
        
    def scan_all_platforms(self, keywords: List[str], industries: List[str]) -> List[Dict]:
        """Scan all enabled platforms for leads"""
        all_leads = []
        
        if self.platforms['reddit']:
            reddit_leads = self.scan_reddit(keywords, industries)
            all_leads.extend(reddit_leads)
        
        # Score and filter
        scored_leads = [self.score_lead(lead) for lead in all_leads]
        high_quality = [lead for lead in scored_leads if lead['score'] >= 70]
        
        return sorted(high_quality, key=lambda x: x['score'], reverse=True)
    
    def scan_reddit(self, keywords: List[str], industries: List[str]) -> List[Dict]:
        """Scan Reddit for high-intent leads"""
        subreddits = [
            'web_design', 'webdev', 'freelance', 'smallbusiness',
            'entrepreneur', 'startups', 'ecommerce', 'shopify',
            'wordpress', 'webhosting'
        ]
        
        leads = []
        
        for subreddit in subreddits:
            try:
                # Fetch new posts
                url = f"https://www.reddit.com/r/{subreddit}/new.json"
                headers = {'User-Agent': 'LeadFlowAI/1.0'}
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    for post in posts:
                        post_data = post.get('data', {})
                        lead = self.analyze_reddit_post(post_data, keywords, industries)
                        
                        if lead:
                            leads.append(lead)
                
                # Rate limit (Reddit allows 60 requests/min)
                time.sleep(1)
                
            except Exception as e:
                print(f"[ERROR] Failed to scan r/{subreddit}: {e}")
                continue
        
        return leads
    
    def analyze_reddit_post(self, post: Dict, keywords: List[str], industries: List[str]) -> Dict:
        """Analyze a Reddit post for lead potential"""
        title = post.get('title', '').lower()
        selftext = post.get('selftext', '').lower()
        combined = f"{title} {selftext}"
        
        # Check if any keywords match
        keyword_match = any(kw.lower() in combined for kw in keywords)
        
        if not keyword_match:
            return None
        
        # Extract signals
        signals = self.extract_signals(combined)
        
        # Must have at least "need help" or "looking for"
        if not signals['intent_signals']:
            return None
        
        return {
            'platform': 'reddit',
            'source': f"r/{post.get('subreddit', 'unknown')}",
            'title': post.get('title', ''),
            'content': post.get('selftext', '')[:500],  # First 500 chars
            'url': f"https://reddit.com{post.get('permalink', '')}",
            'author': post.get('author', '[deleted]'),
            'created_utc': post.get('created_utc', 0),
            'upvotes': post.get('ups', 0),
            'comments': post.get('num_comments', 0),
            'signals': signals,
            'raw_score': 0  # Will be scored
        }
    
    def extract_signals(self, text: str) -> Dict:
        """Extract buying signals from text"""
        signals = {
            'intent_signals': [],
            'budget_signals': [],
            'urgency_signals': [],
            'authority_signals': [],
            'pain_points': []
        }
        
        # Intent signals
        intent_patterns = [
            'looking for', 'need help', 'need a', 'hire', 'recommendations',
            'who can', 'anyone know', 'best way to', 'help with'
        ]
        for pattern in intent_patterns:
            if pattern in text:
                signals['intent_signals'].append(pattern)
        
        # Budget signals
        budget_patterns = [
            r'\$\d+', r'\d+k budget', r'\d+k for', 'willing to pay',
            'budget of', 'can afford', 'price range'
        ]
        for pattern in budget_patterns:
            if re.search(pattern, text):
                signals['budget_signals'].append(pattern)
        
        # Urgency signals
        urgency_patterns = [
            'asap', 'urgent', 'quickly', 'this week', 'soon',
            'immediately', 'deadline', 'by friday'
        ]
        for pattern in urgency_patterns:
            if pattern in text:
                signals['urgency_signals'].append(pattern)
        
        # Authority signals
        authority_patterns = [
            "i'm the founder", "i'm the ceo", "my company", "our startup",
            "my business", "our team", "i own"
        ]
        for pattern in authority_patterns:
            if pattern in text:
                signals['authority_signals'].append(pattern)
        
        # Pain points
        pain_patterns = [
            'struggling', 'problem', 'issue', 'broken', 'not working',
            'frustrated', 'stuck', 'difficult', 'hard to'
        ]
        for pattern in pain_patterns:
            if pattern in text:
                signals['pain_points'].append(pattern)
        
        return signals
    
    def score_lead(self, lead: Dict) -> Dict:
        """Score a lead from 0-100 based on signals"""
        score = 0
        signals = lead.get('signals', {})
        
        # Intent signals (required - base 30 points)
        if signals.get('intent_signals'):
            score += 30
        else:
            lead['score'] = 0
            lead['grade'] = 'F'
            return lead
        
        # Budget signals (20 points)
        if signals.get('budget_signals'):
            score += 20
        
        # Urgency signals (15 points)
        if signals.get('urgency_signals'):
            score += 15
        
        # Authority signals (15 points)
        if signals.get('authority_signals'):
            score += 15
        
        # Pain points (10 points)
        if signals.get('pain_points'):
            score += 10
        
        # Platform engagement (10 points max)
        upvotes = lead.get('upvotes', 0)
        comments = lead.get('comments', 0)
        
        if upvotes > 10:
            score += 5
        if comments > 5:
            score += 5
        
        # Recency (5 points if < 24h old)
        created = lead.get('created_utc', 0)
        age_hours = (time.time() - created) / 3600
        if age_hours < 24:
            score += 5
        
        # Assign grade
        if score >= 85:
            grade = 'A'
        elif score >= 70:
            grade = 'B'
        elif score >= 50:
            grade = 'C'
        else:
            grade = 'D'
        
        lead['score'] = score
        lead['grade'] = grade
        
        return lead
    
    def generate_response_template(self, lead: Dict) -> str:
        """Generate a personalized response template"""
        signals = lead.get('signals', {})
        
        template = f"Hey! I saw your post about [TOPIC].\n\n"
        
        # Empathy based on pain points
        if signals.get('pain_points'):
            template += "I totally get the frustration — [PAIN POINT] can be really challenging.\n\n"
        
        # Value proposition
        template += "I've helped [X SIMILAR CLIENTS] with exactly this. "
        
        # Address urgency
        if signals.get('urgency_signals'):
            template += "I know you're on a timeline, so I can get started immediately.\n\n"
        else:
            template += "\n\n"
        
        # Soft CTA
        template += "Happy to share some quick tips here, or if you want to chat about options, feel free to DM me!\n\n"
        template += "[YOUR SIGNATURE]"
        
        return template


def test_engine():
    """Test the lead generation engine"""
    print("\n🤖 LeadFlow AI - Lead Generation Engine Test\n")
    
    engine = LeadEngine()
    
    # Test keywords for web design agency
    keywords = [
        'website', 'web design', 'web developer', 'build a site',
        'need a website', 'looking for developer', 'hire designer'
    ]
    
    industries = ['web design', 'web development', 'ecommerce']
    
    print("[SCAN] Scanning Reddit for leads...")
    leads = engine.scan_all_platforms(keywords, industries)
    
    print(f"\n[FOUND] {len(leads)} high-quality leads\n")
    
    # Display top 5
    for i, lead in enumerate(leads[:5], 1):
        print(f"[{i}] Grade: {lead['grade']} | Score: {lead['score']}")
        print(f"    Platform: {lead['platform']} ({lead['source']})")
        print(f"    Title: {lead['title'][:80]}...")
        print(f"    URL: {lead['url']}")
        print(f"    Signals: {len(lead['signals']['intent_signals'])} intent, "
              f"{len(lead['signals']['budget_signals'])} budget, "
              f"{len(lead['signals']['urgency_signals'])} urgency")
        print()
    
    # Generate template for top lead
    if leads:
        print("\n[TEMPLATE] Response template for top lead:\n")
        print("="*60)
        print(engine.generate_response_template(leads[0]))
        print("="*60)
    
    return leads


if __name__ == "__main__":
    leads = test_engine()
    
    # Save to file
    output_file = f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    
    print(f"\n[SAVE] Leads saved to: {output_file}")
    print("\n✅ Test complete!\n")
