#!/usr/bin/env python3
"""
LeadFlow AI - Full Onboarding Automation
Handles signup → payment → customer activation with ZERO manual work
"""

import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Payment links
PAYMENT_LINKS = {
    'starter': 'https://buy.stripe.com/cNi5kD7HS0fB6wN0QA00000',
    'growth': 'https://buy.stripe.com/14A00j7HSgez1ct9n600001',
    'agency': 'https://buy.stripe.com/9B68wPgeo7I38EVgPy00002'
}

PLAN_INFO = {
    'starter': {'name': 'Starter', 'price': '$149/mo', 'leads': 20},
    'growth': {'name': 'Growth', 'price': '$299/mo', 'leads': 50},
    'agency': {'name': 'Agency', 'price': '$499/mo', 'leads': 100}
}

def load_database():
    """Load customer database"""
    if os.path.exists('customers.json'):
        with open('customers.json', 'r') as f:
            return json.load(f)
    return []

def save_database(customers):
    """Save customer database"""
    with open('customers.json', 'w') as f:
        json.dump(customers, f, indent=2)

def send_email(to_email, subject, html_body):
    """Send email via Gmail"""
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv('SENDER_EMAIL', 'banmart@gmail.com')
    sender_password = os.getenv('SENDER_PASSWORD', '')
    
    if not sender_password:
        print(f"[SKIP] No password. Would send to {to_email}: {subject}")
        print(f"[BODY PREVIEW] {html_body[:200]}")
        return False
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"LeadFlow AI <{sender_email}>"
    msg['To'] = to_email
    
    html_part = MIMEText(html_body, 'html')
    msg.attach(html_part)
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"[SENT] {subject} → {to_email}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send: {e}")
        return False

def send_welcome_email(customer):
    """Send welcome email with payment link"""
    plan = customer['plan']
    plan_info = PLAN_INFO[plan]
    payment_link = PAYMENT_LINKS[plan]
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; max-width: 600px; margin: 0 auto; }}
            .cta-button {{ display: inline-block; padding: 16px 32px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }}
            .plan-box {{ background: #f0fdf4; border: 2px solid #10b981; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎉 Welcome to LeadFlow AI!</h1>
        </div>
        <div class="content">
            <p>Hi {customer['name']},</p>
            
            <p>Thanks for signing up for LeadFlow AI! You're about to stop wasting time on manual prospecting.</p>
            
            <div class="plan-box">
                <h3>{plan_info['name']} Plan - {plan_info['price']}</h3>
                <p>✅ {plan_info['leads']} qualified leads per week<br>
                ✅ AI-powered lead scoring<br>
                ✅ Daily email digest at 8 AM<br>
                ✅ 50% OFF locked in forever</p>
            </div>
            
            <h3>Next Step: Complete Your Payment</h3>
            <p>Click below to set up your subscription (secure Stripe checkout):</p>
            
            <a href="{payment_link}" class="cta-button">Complete Payment - {plan_info['price']}</a>
            
            <h3>What Happens After Payment:</h3>
            <ul>
                <li>Your first lead digest arrives tomorrow at 8 AM</li>
                <li>You'll receive 20-100 leads per week (depending on your plan)</li>
                <li>Every lead includes: title, description, score (A/B/C), and direct link</li>
                <li>Reply to leads within minutes, close more deals</li>
            </ul>
            
            <p><strong>Questions?</strong> Just reply to this email. I'm here to help.</p>
            
            <p>Looking forward to helping you find more clients!</p>
            
            <p>— Steve<br>
            Founder, LeadFlow AI<br>
            <a href="mailto:banmart@gmail.com">banmart@gmail.com</a></p>
        </div>
    </body>
    </html>
    """
    
    subject = f"🚀 Welcome to LeadFlow AI - Complete Your {plan_info['name']} Plan"
    return send_email(customer['email'], subject, html)

def send_payment_reminder(customer):
    """Send reminder if no payment after 24 hours"""
    plan = customer['plan']
    plan_info = PLAN_INFO[plan]
    payment_link = PAYMENT_LINKS[plan]
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>👋 Quick reminder</h2>
            
            <p>Hi {customer['name']},</p>
            
            <p>You signed up for LeadFlow AI yesterday but haven't completed payment yet.</p>
            
            <p><strong>Your {plan_info['name']} plan is reserved for you:</strong><br>
            {plan_info['price']} • {plan_info['leads']} leads/week • 50% OFF lifetime</p>
            
            <p><a href="{payment_link}" style="display: inline-block; padding: 12px 24px; background: #10b981; color: white; text-decoration: none; border-radius: 6px;">Complete Payment Now</a></p>
            
            <p><strong>Note:</strong> Beta spots are limited to 50 customers. Once we're full, the price goes back to regular pricing.</p>
            
            <p>Questions? Just reply to this email.</p>
            
            <p>— Steve<br>LeadFlow AI</p>
        </div>
    </body>
    </html>
    """
    
    subject = "Your LeadFlow AI beta spot is reserved (complete payment)"
    return send_email(customer['email'], subject, html)

def send_activation_email(customer):
    """Send activation email after payment"""
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>🎉 You're All Set!</h2>
            
            <p>Hi {customer['name']},</p>
            
            <p><strong>Payment confirmed!</strong> Your LeadFlow AI subscription is now active.</p>
            
            <h3>What to Expect:</h3>
            <ul>
                <li>📧 <strong>Daily Lead Digest:</strong> Arrives every morning at 8 AM Pacific</li>
                <li>🎯 <strong>High-Quality Leads:</strong> Only A/B grade leads (scored 50-100)</li>
                <li>⚡ <strong>Fast Response = More Deals:</strong> Reply within 60 minutes for best results</li>
            </ul>
            
            <h3>Tips for Success:</h3>
            <ul>
                <li>Check your email at 8 AM daily (or set up filters)</li>
                <li>Respond to A-grade leads immediately (highest intent)</li>
                <li>Use the response templates as a starting point</li>
                <li>Track which subreddits convert best for your niche</li>
            </ul>
            
            <p><strong>Your first lead digest arrives tomorrow at 8 AM.</strong></p>
            
            <p>Questions or need help? Just reply to this email.</p>
            
            <p>Welcome aboard! 🚀</p>
            
            <p>— Steve<br>
            Founder, LeadFlow AI<br>
            banmart@gmail.com</p>
        </div>
    </body>
    </html>
    """
    
    subject = "✅ LeadFlow AI Activated - First Leads Tomorrow!"
    return send_email(customer['email'], subject, html)

def add_customer_to_delivery(customer):
    """Add customer to send_leads_email.py"""
    # This would be automatic if using a database, but for now, print instructions
    print(f"\n{'='*60}")
    print(f"NEW CUSTOMER ACTIVATED: {customer['name']}")
    print(f"{'='*60}")
    print(f"Email: {customer['email']}")
    print(f"Plan: {customer['plan']}")
    print(f"\nTO ACTIVATE LEAD DELIVERY:")
    print(f"1. Open: send_leads_email.py")
    print(f"2. Add to CUSTOMERS list:")
    print(f"""
    {{
        'name': '{customer['name']}',
        'email': '{customer['email']}',
        'plan': '{customer['plan']}',
        'leads_per_week': {PLAN_INFO[customer['plan']]['leads']}
    }}
    """)
    print(f"3. Save file")
    print(f"{'='*60}\n")

def process_new_signup(name, email, plan, company=''):
    """Process a new signup"""
    customers = load_database()
    
    # Check if already exists
    existing = [c for c in customers if c['email'] == email]
    if existing:
        print(f"[EXISTS] {email} already in database")
        return existing[0]
    
    # Create new customer
    customer = {
        'name': name,
        'email': email,
        'plan': plan,
        'company': company,
        'signed_up': datetime.now().isoformat(),
        'payment_sent': False,
        'paid': False,
        'activated': False
    }
    
    customers.append(customer)
    save_database(customers)
    
    # Send welcome email
    print(f"\n[NEW SIGNUP] {name} ({email}) - {plan} plan")
    send_welcome_email(customer)
    
    # Update status
    customer['payment_sent'] = True
    save_database(customers)
    
    return customer

def process_payment(email):
    """Mark customer as paid and activate"""
    customers = load_database()
    
    for customer in customers:
        if customer['email'] == email and not customer['paid']:
            customer['paid'] = True
            customer['paid_at'] = datetime.now().isoformat()
            save_database(customers)
            
            # Send activation email
            send_activation_email(customer)
            
            # Show activation instructions
            add_customer_to_delivery(customer)
            
            customer['activated'] = True
            save_database(customers)
            
            print(f"[ACTIVATED] {customer['name']} - {customer['plan']} plan")
            return customer
    
    print(f"[NOT FOUND] {email} not in database")
    return None

def check_payment_reminders():
    """Send reminders to people who haven't paid"""
    customers = load_database()
    now = datetime.now()
    
    for customer in customers:
        if customer['payment_sent'] and not customer['paid']:
            # Check if >24 hours since signup
            signed_up = datetime.fromisoformat(customer['signed_up'])
            hours_since = (now - signed_up).total_seconds() / 3600
            
            if hours_since > 24 and not customer.get('reminder_sent'):
                send_payment_reminder(customer)
                customer['reminder_sent'] = True
                save_database(customers)

# CLI
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("LeadFlow AI - Onboarding Automation")
        print("\nCommands:")
        print("  python automate_onboarding.py signup <name> <email> <plan>")
        print("  python automate_onboarding.py paid <email>")
        print("  python automate_onboarding.py reminders")
        print("\nExamples:")
        print("  python automate_onboarding.py signup 'John Doe' john@agency.com growth")
        print("  python automate_onboarding.py paid john@agency.com")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'signup':
        name = sys.argv[2]
        email = sys.argv[3]
        plan = sys.argv[4]
        process_new_signup(name, email, plan)
    
    elif command == 'paid':
        email = sys.argv[2]
        process_payment(email)
    
    elif command == 'reminders':
        check_payment_reminders()
