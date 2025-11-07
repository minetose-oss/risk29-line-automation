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
DASHBOARD_URL = "https://minetose-oss.github.io/risk29-dashboard"
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

def get_risk_level_color(score):
    """Get color based on risk score"""
    if score >= 70:
        return "#EF4444"  # Red - High Risk
    elif score >= 40:
        return "#F59E0B"  # Orange - Medium Risk
    else:
        return "#10B981"  # Green - Low Risk

def get_risk_level_text(score):
    """Get risk level text"""
    if score >= 70:
        return "Alert"
    elif score >= 60:
        return "Warning"
    elif score >= 40:
        return "Watch"
    else:
        return "Info"

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

def create_flex_message(data):
    """Create LINE Flex Message with dashboard design"""
    # Get current time in GMT+7
    tz = pytz.timezone('Asia/Bangkok')
    now = datetime.now(tz)
    date_str = now.strftime('%Y-%m-%d')
    
    # Calculate metrics
    overall_risk = calculate_overall_risk(data)
    overall_color = get_risk_level_color(overall_risk)
    risk_level = get_risk_level_text(overall_risk)
    
    # Get all categories with scores
    categories = data.get('categories', {})
    category_items = []
    
    # Category display names and emojis
    category_info = {
        'liquidity': {'name': 'Liquidity', 'emoji': '💧'},
        'valuation': {'name': 'Valuation', 'emoji': '📊'},
        'credit': {'name': 'Credit', 'emoji': '💳'},
        'macro': {'name': 'Macro', 'emoji': '📈'},
        'global': {'name': 'Global', 'emoji': '🌐'},
        'technical': {'name': 'Technical', 'emoji': '🔧'},
        'sentiment': {'name': 'Sentiment', 'emoji': '😊'},
        'qualitative': {'name': 'Qualitative', 'emoji': '📋'}
    }
    
    # Sort categories by score (highest first)
    sorted_cats = sorted(categories.items(), key=lambda x: x[1].get('score', 0), reverse=True)
    
    for cat_key, cat_data in sorted_cats:
        score = cat_data.get('score', 0)
        info = category_info.get(cat_key, {'name': cat_key.capitalize(), 'emoji': '📌'})
        color = get_risk_level_color(score)
        
        category_items.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": f"{info['emoji']} {info['name']}",
                    "size": "sm",
                    "color": "#666666",
                    "flex": 3
                },
                {
                    "type": "text",
                    "text": str(int(score)),
                    "size": "sm",
                    "color": color,
                    "align": "end",
                    "weight": "bold",
                    "flex": 1
                }
            ],
            "margin": "md"
        })
    
    # Get top 3 risks for highlights
    top_risks = get_top_risk_categories(data, 3)
    top_risk_text = "\n".join([
        f"• {category_info.get(cat, {'name': cat.capitalize()})['name']} ~{int(score)}"
        for cat, score in top_risks
    ])
    
    # Create Flex Message
    flex_message = {
        "type": "flex",
        "altText": f"🎯 Risk29 Morning Summary - Overall Risk: {overall_risk}/100",
        "contents": {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📊 RISK-29",
                                "color": "#FFFFFF",
                                "size": "xl",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": risk_level,
                                "color": "#FFFFFF",
                                "size": "xs",
                                "align": "end",
                                "gravity": "center"
                            }
                        ]
                    }
                ],
                "backgroundColor": "#1E40AF",
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "ระดับความเสี่ยง",
                                "size": "sm",
                                "color": "#666666"
                            },
                            {
                                "type": "text",
                                "text": "คะแนนรวม",
                                "size": "xs",
                                "color": "#999999",
                                "margin": "xs"
                            },
                            {
                                "type": "text",
                                "text": f"{overall_risk} / 100",
                                "size": "xxl",
                                "weight": "bold",
                                "color": overall_color,
                                "margin": "md"
                            }
                        ],
                        "backgroundColor": "#F3F4F6",
                        "paddingAll": "15px",
                        "cornerRadius": "8px"
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📈 คะแนนตามหมวด",
                                "size": "md",
                                "weight": "bold",
                                "color": "#1F2937"
                            }
                        ] + category_items,
                        "margin": "xl"
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "⚠️ จุดเสี่ยงสูงสุด",
                                "size": "md",
                                "weight": "bold",
                                "color": "#1F2937"
                            },
                            {
                                "type": "text",
                                "text": top_risk_text,
                                "size": "sm",
                                "color": "#666666",
                                "wrap": True,
                                "margin": "md"
                            }
                        ],
                        "margin": "xl"
                    }
                ],
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"📅 {date_str}",
                                "size": "xs",
                                "color": "#999999"
                            },
                            {
                                "type": "text",
                                "text": "Risk29 Free-Real PLUS",
                                "size": "xs",
                                "color": "#999999",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "ดูแดชบอร์ดแบบเต็ม",
                            "uri": DASHBOARD_URL
                        },
                        "style": "primary",
                        "color": "#10B981",
                        "margin": "md"
                    }
                ],
                "paddingAll": "20px"
            }
        }
    }
    
    return flex_message

def send_line_message(message, channel_access_token, user_id):
    """Send message via LINE Messaging API"""
    headers = {
        'Authorization': f'Bearer {channel_access_token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'to': user_id,
        'messages': [message]
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
    
    # Create Flex Message
    print("🎨 Creating dashboard Flex Message...")
    flex_message = create_flex_message(risk_data)
    print("✅ Flex Message created")
    
    # Send to LINE
    print("\n📤 Sending to LINE Messaging API...")
    success = send_line_message(flex_message, channel_access_token, user_id)
    
    if success:
        print("\n🎉 Daily report sent successfully!")
        return True
    else:
        print("\n❌ Failed to send daily report")
        return False

if __name__ == "__main__":
    exit(0 if main() else 1)
