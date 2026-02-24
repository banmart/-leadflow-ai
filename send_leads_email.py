#!/usr/bin/env python3
"""
LeadFlow AI - Daily Lead Email Sender
Sends daily digest of leads to paying customers
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Customer list (add new customers here)
CUSTOMERS = [
    {
        'name': 'Test Customer',
        'email': 'banmart@gmail.com',  # Replace with actual customer
        'plan': 'growth',
        'leads_per_week': 50
    }
]

def load_leads():
    """Load leads from JSON"""
    try:
        with open('leads.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def format_lead_email(leads, customer_name):
    """Generate HTML email with leads"""
    
    # Filter to top leads only
    top_leads = [l for l in leads if l['grade'] in ['A', 'B']][:10]
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
            .lead {{ border: 1px solid #e5e7eb; padding: 20px; margin: 20px 0; border-radius: 8px; }}
            .grade-A {{ border-left: 4px solid #10b981; }}
            .grade-B {{ border-left: 4px solid #f59e0b; }}
            .grade {{ font-weight: bold; font-size: 18px; }}
            .grade-A .grade {{ color: #10b981; }}
            .grade-B .grade {{ color: #f59e0b; }}
            .title {{ font-size: 18px; font-weight: 600; margin: 10px 0; }}
            .meta {{ color: #6b7280; font-size: 14px; }}
            .text {{ margin: 15px 0; padding: 15px; background: #f9fafb; border-radius: 6px; }}
            .cta {{ display: inline-block; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 6px; margin-top: 10px; }}
            .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 14px; margin-top: 40px; border-top: 1px solid #e5e7eb; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 Your Daily Leads from LeadFlow AI</h1>
            <p>Hi {customer_name}, here are today's top opportunities</p>
        </div>
        
        <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
            <p><strong>{len(top_leads)} High-Quality Leads Found</strong></p>
            <p>Grade A = High intent + budget signals + urgency<br>
            Grade B = Good intent, worth checking</p>
    """
    
    for i, lead in enumerate(top_leads, 1):
        html += f"""
            <div class="lead grade-{lead['grade']}">
                <div class="grade">#{i} - Grade {lead['grade']} ({lead['score']}/100)</div>
                <div class="title">{lead['title']}</div>
                <div class="meta">r/{lead['subreddit']} • u/{lead['author']} • {lead['created']}</div>
                <div class="text">{lead['text'][:300]}{'...' if len(lead['text']) > 300 else ''}</div>
                <a href="{lead['url']}" class="cta" target="_blank">View on Reddit →</a>
            </div>
        """
    
    html += f"""
            <div class="footer">
                <p>You're on the <strong>Growth Plan</strong> - 50 leads/week</p>
                <p>Questions? Reply to this email or contact support.</p>
                <p style="margin-top: 20px;">
                    <a href="https://leadsflowbot.com" style="color: #667eea;">LeadFlow AI</a> | 
                    <a href="mailto:banmart@gmail.com" style="color: #667eea;">Support</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def send_email(to_email, subject, html_body):
    """Send email via Gmail SMTP"""
    
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv('SENDER_EMAIL', 'banmart@gmail.com')
    sender_password = os.getenv('SENDER_PASSWORD', '')  # App password needed
    
    if not sender_password:
        print(f"[SKIP] No SENDER_PASSWORD set. Would send to: {to_email}")
        print(f"[SUBJECT] {subject}")
        print(f"[PREVIEW] {len(html_body)} chars")
        return False
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"LeadFlow AI <{sender_email}>"
    msg['To'] = to_email
    
    # Attach HTML
    html_part = MIMEText(html_body, 'html')
    msg.attach(html_part)
    
    # Send
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        
        print(f"[SENT] Email to {to_email}")
        return True
    
    except Exception as e:
        print(f"[ERROR] Failed to send to {to_email}: {e}")
        return False

def send_daily_digest():
    """Send daily lead digest to all customers"""
    
    leads = load_leads()
    
    if not leads:
        print("[INFO] No leads to send")
        return
    
    print(f"[START] Sending daily digest with {len(leads)} leads")
    
    for customer in CUSTOMERS:
        subject = f"🚀 {len([l for l in leads if l['grade'] in ['A','B']])} New Leads for {datetime.now().strftime('%B %d, %Y')}"
        html_body = format_lead_email(leads, customer['name'])
        
        send_email(customer['email'], subject, html_body)
    
    print("[DONE] Daily digest sent")

if __name__ == '__main__':
    send_daily_digest()
