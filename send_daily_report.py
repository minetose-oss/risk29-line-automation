#!/usr/bin/env python3
"""
Risk29 Daily Morning Report - LINE Messaging API
Sends automated daily risk summary to LINE via Messaging API at 8 AM GMT+7
"""

import os
import json
import requests
from datetime import datetime
import pytz

# Configuration
DASHBOARD_URL = "https://riskdash-h38zfvrd.manus.space"
RISK_DATA_URL = f"{DASHBOARD_URL}/risk_data.json"
LINE_MESSAGING_API = "https://api.line.me/v2/bot/message/push"

def get_risk_data():
    """Fetch risk data from dashboard"""
    try:
        response = requests.get(RISK_DATA_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching risk data: {e}")
        return None

def calculate_overall_risk(data):
    """Calculate weighted overall risk score"""
    if not data or 'categories' not in data:
        return 0
    
    categories = data['categories']
    weights = data.get('weights', {})
    
    total_score = 0
    total_weight = 0
    
    for category, category_data in categories.items():
        weight = weights.get(category, 1.0)
        score = category_data.get('score', 0)
        total_score += score * weight
        total_weight += weight
    
    return round(total_score / total_weight if total_weight > 0 else 0, 1)

def get_top_risk_categories(data, top_n=3):
    """Get top N highest risk categories"""
    if not data or 'categories' not in data:
        return []
    
    categories = data['categories']
    sorted_categories = sorted(
        categories.items(),
        key=lambda x: x[1].get('score', 0),
        reverse=True
    )
    
    return [(name, cat_data.get('score', 0)) for name, cat_data in sorted_categories[:top_n]]

def count_signals_by_risk(data):
    """Count signals by risk level"""
    if not data or 'categories' not in data:
        return {'high': 0, 'medium': 0, 'low': 0, 'total': 0}
    
    high_count = 0
    medium_count = 0
    low_count = 0
    total_count = 0
    
    for category_data in data['categories'].values():
        signals = category_data.get('signals', [])
        for signal in signals:
            total_count += 1
            score = signal.get('score', 0)
            if score >= 70:
                high_count += 1
            elif score >= 40:
                medium_count += 1
            else:
                low_count += 1
    
    return {
        'high': high_count,
        'medium': medium_count,
        'low': low_count,
        'total': total_count
    }

def format_message(data):
    """Format risk summary message for LINE"""
    # Get current time in GMT+7
    tz = pytz.timezone('Asia/Bangkok')
    now = datetime.now(tz)
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M')
    
    # Calculate metrics
    overall_risk = calculate_overall_risk(data)
    top_categories = get_top_risk_categories(data)
    signal_counts = count_signals_by_risk(data)
    
    # Format category names with emojis
    category_emojis = {
        'liquidity': '💧',
        'valuation': '📊',
        'macro': '🌍',
        'credit': '💳',
        'technical': '🔧',
        'sentiment': '😊',
        'qualitative': '📋',
        'global': '🌐'
    }
    
    # Build message
    message = f"""🎯 Risk29 Morning Summary
📅 {date_str} {time_str}

📊 Overall Risk Score: {overall_risk}/100

⚠️ Top Risk Categories:"""
    
    for cat_name, score in top_categories:
        emoji = category_emojis.get(cat_name.lower(), '📌')
        display_name = cat_name.capitalize()
        message += f"\n• {emoji} {display_name}: {score}"
    
    message += f"""

📈 Signal Summary:
• High Risk: {signal_counts['high']} signals
• Medium Risk: {signal_counts['medium']} signals
• Low Risk: {signal_counts['low']} signals

Total Signals Analyzed: {signal_counts['total']}

✅ Pipeline executed successfully"""
    
    return message

def send_line_message(message, channel_access_token, user_id):
    """Send message via LINE Messaging API"""
    headers = {
        'Authorization': f'Bearer {channel_access_token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'to': user_id,
        'messages': [
            {
                'type': 'text',
                'text': message
            }
        ]
    }
    
    try:
        response = requests.post(LINE_MESSAGING_API, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        print(f"✅ LINE message sent successfully at {datetime.now()}")
        return True
    except Exception as e:
        print(f"❌ Error sending LINE message: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

def main():
    """Main execution function"""
    print("=" * 50)
    print("Risk29 Daily Morning Report")
    print("=" * 50)
    
    # Get LINE credentials from environment variables
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    user_id = os.getenv('LINE_USER_ID')
    
    if not channel_access_token:
        print("❌ ERROR: LINE_CHANNEL_ACCESS_TOKEN environment variable not set")
        print("Please set it in GitHub Secrets")
        return False
    
    if not user_id:
        print("❌ ERROR: LINE_USER_ID environment variable not set")
        print("Please set it in GitHub Secrets")
        return False
    
    # Fetch risk data
    print("📡 Fetching risk data from dashboard...")
    risk_data = get_risk_data()
    
    if not risk_data:
        print("❌ Failed to fetch risk data")
        return False
    
    print("✅ Risk data fetched successfully")
    
    # Format message
    print("📝 Formatting message...")
    message = format_message(risk_data)
    print("\nMessage to send:")
    print("-" * 50)
    print(message)
    print("-" * 50)
    
    # Send to LINE
    print("\n📤 Sending to LINE Messaging API...")
    success = send_line_message(message, channel_access_token, user_id)
    
    if success:
        print("\n🎉 Daily report sent successfully!")
        return True
    else:
        print("\n❌ Failed to send daily report")
        return False

if __name__ == "__main__":
    exit(0 if main() else 1)
