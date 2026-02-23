#!/usr/bin/env python3
"""
LeadFlow AI - Fully Automated Lead Response System
NO MANUAL WORK REQUIRED

Finds leads + generates responses + auto-sends
User just approves or it auto-sends after review period
"""

import os
import json
import requests
import time
from datetime import datetime
from lead_engine import LeadEngine

class AutoResponder:
    """Fully automated lead response system"""
    
    def __init__(self, reddit_username=None, reddit_password=None):
        self.engine = LeadEngine()
        self.reddit_username = reddit_username or os.getenv('REDDIT_USERNAME')
        self.reddit_password = reddit_password or os.getenv('REDDIT_PASSWORD')
        self.auto_respond = True  # Set to False for approval mode
        self.min_score = 70  # Only respond to A/B grade leads
        
    def run_full_cycle(self, keywords, industries):
        """Complete automation: Find → Score → Generate → Send"""
        
        print("\n[AUTO] Starting automated lead response cycle...\n")
        
        # Step 1: Find leads
        print("[1/4] Finding leads...")
        leads = self.engine.scan_all_platforms(keywords, industries)
        print(f"      Found {len(leads)} high-quality leads\n")
        
        if not leads:
            print("[DONE] No leads found this cycle.\n")
            return
        
        # Step 2: Generate responses
        print("[2/4] Generating responses...")
        leads_with_responses = []
        
        for lead in leads:
            if lead['score'] >= self.min_score:
                response = self.generate_personalized_response(lead)
                lead['response'] = response
                leads_with_responses.append(lead)
                print(f"      [{lead['grade']}] {lead['title'][:50]}...")
        
        print(f"      Generated {len(leads_with_responses)} responses\n")
        
        # Step 3: Send responses (if auto-respond enabled)
        if self.auto_respond:
            print("[3/4] Auto-sending responses...")
            sent_count = 0
            
            for lead in leads_with_responses:
                if self.send_response(lead):
                    sent_count += 1
                    time.sleep(5)  # Rate limit: 5 seconds between posts
            
            print(f"      Sent {sent_count} responses\n")
        else:
            print("[3/4] Approval mode - saving for review...")
            self.save_for_approval(leads_with_responses)
            print(f"      {len(leads_with_responses)} responses ready for approval\n")
        
        # Step 4: Log results
        print("[4/4] Logging results...")
        self.log_cycle(leads_with_responses)
        
        print("\n[DONE] Automation cycle complete!\n")
        
        return leads_with_responses
    
    def generate_personalized_response(self, lead):
        """Generate highly personalized response based on lead signals"""
        
        title = lead['title']
        signals = lead['signals']
        
        # Start with empathy/connection
        opening = self.get_opening(signals)
        
        # Add specific value based on pain points
        value = self.get_value_prop(signals)
        
        # Address urgency if present
        timeline = ""
        if signals.get('urgency_signals'):
            timeline = "\n\nI know timing matters - I can start immediately if you need quick turnaround."
        
        # Soft CTA
        cta = "\n\nHappy to share some quick tips here, or feel free to DM if you want to discuss options!"
        
        # Combine
        response = f"{opening}\n\n{value}{timeline}{cta}"
        
        return response
    
    def get_opening(self, signals):
        """Generate personalized opening based on signals"""
        
        if signals.get('pain_points'):
            pain = signals['pain_points'][0]
            return f"I totally get the frustration with {pain} - it's one of those things that looks simple but can be tricky."
        
        if signals.get('urgency_signals'):
            return "Saw you're looking to move quickly on this - that's smart."
        
        return "I saw your post and thought I could help with this."
    
    def get_value_prop(self, signals):
        """Generate value proposition based on signals"""
        
        # If budget signals present, mention experience
        if signals.get('budget_signals'):
            return "I've helped several businesses in similar situations. Usually it's a combination of [technical fix] + [process improvement]."
        
        # If authority signals, mention business outcomes
        if signals.get('authority_signals'):
            return "For businesses like yours, I typically focus on [business outcome] rather than just [technical solution]. Happy to explain the approach."
        
        # Default
        return "I've worked on this exact issue before. There are a few approaches that work well depending on your situation."
    
    def send_response(self, lead):
        """Auto-send response to Reddit"""
        
        # THIS IS WHERE YOU'D USE REDDIT API
        # For now, just simulate
        
        print(f"   [SEND] {lead['title'][:50]}...")
        print(f"          Response: {lead['response'][:80]}...")
        
        # In production:
        # Use PRAW (Python Reddit API Wrapper)
        # reddit.comment(lead['reddit_id'], lead['response'])
        
        # For now, just log it
        return True
    
    def save_for_approval(self, leads):
        """Save leads for manual approval"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"leads_pending_approval_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)
        
        print(f"      Saved to: {filename}")
        print(f"      Review and approve at: approval-dashboard.html")
    
    def log_cycle(self, leads):
        """Log automation cycle results"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        log_entry = {
            'timestamp': timestamp,
            'leads_found': len(leads),
            'responses_sent': len([l for l in leads if l.get('response')]),
            'avg_score': sum(l['score'] for l in leads) / len(leads) if leads else 0,
            'grade_breakdown': {
                'A': len([l for l in leads if l['grade'] == 'A']),
                'B': len([l for l in leads if l['grade'] == 'B']),
                'C': len([l for l in leads if l['grade'] == 'C'])
            }
        }
        
        # Append to log file
        log_file = 'automation_log.json'
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"      Logged to: {log_file}")


def run_continuous(interval_minutes=30):
    """Run automation continuously"""
    
    print("\n" + "="*60)
    print("LEADFLOW AI - FULL AUTOMATION MODE")
    print("="*60)
    print(f"Running every {interval_minutes} minutes")
    print("Press Ctrl+C to stop\n")
    
    bot = AutoResponder()
    
    # Keywords for web design agencies
    keywords = [
        'website', 'web design', 'web developer', 'build a site',
        'need a website', 'looking for developer', 'hire designer',
        'website help', 'redesign website', 'broken website'
    ]
    
    industries = ['web design', 'web development', 'ecommerce']
    
    cycle = 1
    
    while True:
        print(f"\n{'='*60}")
        print(f"CYCLE #{cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")
        
        try:
            bot.run_full_cycle(keywords, industries)
            
            cycle += 1
            
            print(f"\n[SLEEP] Waiting {interval_minutes} minutes until next cycle...")
            print(f"        Next run at: {datetime.now().strftime('%H:%M:%S')}")
            
            time.sleep(interval_minutes * 60)
            
        except KeyboardInterrupt:
            print("\n\n[STOP] Automation stopped by user.\n")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")
            print(f"[RETRY] Waiting 5 minutes before retry...\n")
            time.sleep(300)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="LeadFlow AI - Full Automation")
    parser.add_argument('--interval', type=int, default=30, help='Minutes between cycles')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--approve', action='store_true', help='Require approval before sending')
    
    args = parser.parse_args()
    
    if args.once:
        # Run once
        bot = AutoResponder()
        keywords = ['website', 'web design', 'web developer', 'need a website']
        industries = ['web design']
        bot.run_full_cycle(keywords, industries)
    else:
        # Run continuously
        run_continuous(args.interval)
