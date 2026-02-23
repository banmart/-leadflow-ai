#!/usr/bin/env python3
"""
LeadFlow AI Launch Campaign - Automated Twitter Content
Run once to post launch thread + schedule Week 1 content
"""

import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from twitter_bot import TwitterBot

load_dotenv()

def launch_now():
    """Post the launch thread immediately"""
    print("\n🚀 LAUNCHING LEADFLOW AI ON TWITTER\n")
    
    bot = TwitterBot()
    
    # Load launch content
    with open('launch_content.json', 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    # Post launch thread
    print("[LAUNCH] Posting launch thread...")
    thread = content['launch_thread']
    bot.post_thread(thread)
    
    print("\n✅ Launch thread posted!")
    print("🔗 Check: https://twitter.com/leadsflowbot")
    
    return True

def schedule_week_1():
    """Schedule Week 1 content (3 posts/day)"""
    print("\n📅 SCHEDULING WEEK 1 CONTENT\n")
    
    with open('launch_content.json', 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    queue = []
    now = datetime.now()
    
    # Day 1: Launch thread (already posted)
    # Day 2-7: Mix of tips, engagement, product updates
    
    schedule = [
        # Day 2
        (1, 9, content['daily_tips'][0]),
        (1, 14, content['engagement_posts'][0]),
        (1, 18, content['customer_success'][0]),
        
        # Day 3
        (2, 9, content['daily_tips'][1]),
        (2, 14, content['engagement_posts'][1]),
        (2, 18, content['product_updates'][0]),
        
        # Day 4
        (3, 9, content['daily_tips'][2]),
        (3, 14, content['customer_success'][1]),
        (3, 18, content['engagement_posts'][2]),
        
        # Day 5
        (4, 9, content['daily_tips'][3]),
        (4, 14, content['product_updates'][1]),
        (4, 18, content['engagement_posts'][3]),
        
        # Day 6
        (5, 9, content['daily_tips'][4]),
        (5, 14, "🎯 Week 1 Update:\n\n✅ 5 beta customers signed up\n✅ $745 MRR\n✅ 2 A-grade leads found\n\n42 spots left at 50% discount.\n\nJoin now: https://leadsflowbot.com"),
        (5, 18, "Weekend question:\n\nWhat's the one marketing task you wish you could automate?\n\nBe honest 👇"),
        
        # Day 7
        (6, 10, "🧵 Sunday Thread: How We Built LeadFlow AI\n\n1/ Started with a simple question:\n\n\"Why do I waste 15 hours/week looking for leads?\"\n\nThere had to be a better way...",),
        (6, 16, "🔥 Last call for Week 1 beta pricing!\n\n50% lifetime discount ends tonight.\n\n35 spots remaining.\n\nJoin: https://leadsflowbot.com\n\n(Yes, lifetime means forever)"),
    ]
    
    for days_offset, hour, text in schedule:
        post_time = now + timedelta(days=days_offset)
        post_time = post_time.replace(hour=hour, minute=0, second=0, microsecond=0)
        
        queue.append({
            'text': text,
            'post_at': post_time.timestamp(),
            'thread': False
        })
    
    # Save queue
    with open('twitter_queue.json', 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=2)
    
    print(f"✅ Scheduled {len(queue)} tweets for Week 1")
    print("\nSchedule:")
    for item in queue[:3]:
        dt = datetime.fromtimestamp(item['post_at'])
        print(f"  {dt.strftime('%a %b %d, %I:%M %p')}: {item['text'][:50]}...")
    print(f"  ... and {len(queue) - 3} more")
    
    print("\n💡 Run 'python twitter_bot.py queue' every hour to post scheduled content")
    print("   Or set up Windows Task Scheduler to run it automatically")

def show_queue():
    """Show upcoming scheduled posts"""
    if not os.path.exists('twitter_queue.json'):
        print("No scheduled posts yet. Run 'launch_campaign.py schedule' first.")
        return
    
    with open('twitter_queue.json', 'r', encoding='utf-8') as f:
        queue = json.load(f)
    
    print(f"\n📅 {len(queue)} SCHEDULED POSTS\n")
    
    for i, item in enumerate(queue, 1):
        dt = datetime.fromtimestamp(item['post_at'])
        print(f"{i}. {dt.strftime('%a %b %d, %I:%M %p')}")
        print(f"   {item['text'][:80]}...")
        print()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("LeadFlow AI Launch Campaign")
        print("\nCommands:")
        print("  python launch_campaign.py launch    - Post launch thread NOW")
        print("  python launch_campaign.py schedule  - Schedule Week 1 content")
        print("  python launch_campaign.py show      - Show scheduled posts")
        print("  python launch_campaign.py all       - Launch + schedule everything")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'launch':
        launch_now()
    
    elif command == 'schedule':
        schedule_week_1()
    
    elif command == 'show':
        show_queue()
    
    elif command == 'all':
        if input("🚀 Launch LeadFlow AI on Twitter now? (yes/no): ").lower() == 'yes':
            launch_now()
            print("\n" + "="*50 + "\n")
            schedule_week_1()
            print("\n✅ LAUNCH COMPLETE!")
        else:
            print("Cancelled.")
    
    else:
        print(f"Unknown command: {command}")
