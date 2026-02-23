#!/usr/bin/env python3
"""
LeadFlow AI Twitter Bot - Full Automation
Handles posting, scheduling, and engagement for @leadsflowbot
"""

import os
import tweepy
from datetime import datetime
import json
import time

class TwitterBot:
    def __init__(self):
        """Initialize Twitter API connection"""
        # Load credentials from environment
        api_key = os.getenv('TWITTER_API_KEY')
        api_secret = os.getenv('TWITTER_API_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_secret = os.getenv('TWITTER_ACCESS_SECRET')
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        if not all([api_key, api_secret, access_token, access_secret]):
            raise ValueError("Missing Twitter API credentials. Check .env file.")
        
        # Twitter API v2 client
        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        
        print(f"[BOT] Connected to Twitter as @leadsflowbot")
    
    def post_tweet(self, text, reply_to_id=None):
        """Post a tweet or reply"""
        try:
            response = self.client.create_tweet(
                text=text,
                in_reply_to_tweet_id=reply_to_id
            )
            tweet_id = response.data['id']
            print(f"[POSTED] Tweet ID: {tweet_id}")
            print(f"[TEXT] {text[:100]}...")
            return tweet_id
        except Exception as e:
            print(f"[ERROR] Failed to post: {e}")
            return None
    
    def post_thread(self, tweets):
        """Post a thread of tweets"""
        print(f"[THREAD] Posting {len(tweets)} tweets...")
        reply_to = None
        tweet_ids = []
        
        for i, text in enumerate(tweets, 1):
            print(f"[THREAD] Tweet {i}/{len(tweets)}")
            tweet_id = self.post_tweet(text, reply_to_id=reply_to)
            if tweet_id:
                tweet_ids.append(tweet_id)
                reply_to = tweet_id
                if i < len(tweets):
                    time.sleep(2)  # Rate limit buffer
            else:
                print(f"[ERROR] Thread stopped at tweet {i}")
                break
        
        return tweet_ids
    
    def get_mentions(self, limit=10):
        """Get recent mentions"""
        try:
            me = self.client.get_me()
            mentions = self.client.get_users_mentions(
                id=me.data.id,
                max_results=limit,
                tweet_fields=['created_at', 'author_id']
            )
            
            if mentions.data:
                print(f"[MENTIONS] Found {len(mentions.data)} mentions")
                return mentions.data
            else:
                print("[MENTIONS] No new mentions")
                return []
        except Exception as e:
            print(f"[ERROR] Failed to get mentions: {e}")
            return []
    
    def search_tweets(self, query, limit=10):
        """Search for tweets matching query"""
        try:
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=limit,
                tweet_fields=['created_at', 'author_id', 'public_metrics']
            )
            
            if tweets.data:
                print(f"[SEARCH] Found {len(tweets.data)} tweets for: {query}")
                return tweets.data
            else:
                print(f"[SEARCH] No tweets found for: {query}")
                return []
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            return []

def load_queue(queue_file='twitter_queue.json'):
    """Load scheduled tweets from queue"""
    if os.path.exists(queue_file):
        with open(queue_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_queue(queue, queue_file='twitter_queue.json'):
    """Save tweet queue to file"""
    with open(queue_file, 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=2)

def process_queue(bot):
    """Post any scheduled tweets that are due"""
    queue = load_queue()
    now = datetime.now().timestamp()
    remaining = []
    
    for item in queue:
        if item['post_at'] <= now:
            print(f"[QUEUE] Posting scheduled tweet...")
            if item.get('thread'):
                bot.post_thread(item['text'])
            else:
                bot.post_tweet(item['text'])
        else:
            remaining.append(item)
    
    if len(remaining) < len(queue):
        save_queue(remaining)
        print(f"[QUEUE] Posted {len(queue) - len(remaining)} tweets, {len(remaining)} remaining")

# Command-line interface
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python twitter_bot.py post 'Your tweet text'")
        print("  python twitter_bot.py thread 'Tweet 1' 'Tweet 2' 'Tweet 3'")
        print("  python twitter_bot.py mentions")
        print("  python twitter_bot.py search 'query'")
        print("  python twitter_bot.py queue")
        sys.exit(1)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    bot = TwitterBot()
    command = sys.argv[1]
    
    if command == 'post':
        bot.post_tweet(sys.argv[2])
    
    elif command == 'thread':
        tweets = sys.argv[2:]
        bot.post_thread(tweets)
    
    elif command == 'mentions':
        mentions = bot.get_mentions()
        for m in mentions:
            print(f"\n@{m.author_id}: {m.text}")
    
    elif command == 'search':
        results = bot.search_tweets(sys.argv[2])
        for t in results:
            print(f"\n{t.text}")
    
    elif command == 'queue':
        process_queue(bot)
    
    else:
        print(f"Unknown command: {command}")
