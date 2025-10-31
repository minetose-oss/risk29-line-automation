#!/usr/bin/env python3
"""
Demo script to show what the LINE message will look like
(Without actually sending to LINE)
"""

import json
import requests
from datetime import datetime
import pytz

DASHBOARD_URL = "https://riskdash-h38zfvrd.manus.space"
RISK_DATA_URL = f"{DASHBOARD_URL}/risk_data.json"

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
    tz = pytz.timezone('Asia/Bangkok')
    now = datetime.now(tz)
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M')
    
    overall_risk = calculate_overall_risk(data)
    top_categories = get_top_risk_categories(data)
    signal_counts = count_signals_by_risk(data)
    
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

print("=" * 60)
print("DEMO: Risk29 Daily Morning Report")
print("=" * 60)
print("\n📡 Fetching risk data from dashboard...")

risk_data = get_risk_data()

if risk_data:
    print("✅ Risk data fetched successfully\n")
    print("=" * 60)
    print("MESSAGE PREVIEW (This will be sent to LINE):")
    print("=" * 60)
    print()
    message = format_message(risk_data)
    print(message)
    print()
    print("=" * 60)
    print("✅ Demo completed successfully!")
    print("=" * 60)
else:
    print("❌ Failed to fetch risk data")
