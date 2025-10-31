#!/usr/bin/env python3
"""
Risk29 Alert Checker - LINE Messaging API
Checks risk levels every 30 minutes and sends alerts when thresholds are exceeded
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
ALERT_STATE_FILE = "/tmp/risk29_alert_state.json"

# Alert thresholds
OVERALL_RISK_THRESHOLD = 60
CATEGORY_RISK_THRESHOLD = 70

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

def check_alert_conditions(data):
    """Check if alert conditions are met"""
    overall_risk = calculate_overall_risk(data)
    categories = data.get('categories', {})
    
    # Check overall risk threshold
    overall_alert = overall_risk >= OVERALL_RISK_THRESHOLD
    
    # Check category thresholds
    high_risk_categories = []
    for cat_name, cat_data in categories.items():
        score = cat_data.get('score', 0)
        if score >= CATEGORY_RISK_THRESHOLD:
            high_risk_categories.append((cat_name, score))
    
    category_alert = len(high_risk_categories) > 0
    
    return {
        'should_alert': overall_alert or category_alert,
        'overall_risk': overall_risk,
        'overall_alert': overall_alert,
        'high_risk_categories': high_risk_categories,
        'category_alert': category_alert
    }

def load_alert_state():
    """Load previous alert state"""
    try:
        if os.path.exists(ALERT_STATE_FILE):
            with open(ALERT_STATE_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {'last_alert_sent': None, 'alert_active': False}

def save_alert_state(state):
    """Save current alert state"""
    try:
        with open(ALERT_STATE_FILE, 'w') as f:
            json.dump(state, f)
    except Exception as e:
        print(f"Warning: Could not save alert state: {e}")

def create_alert_flex_message(data, alert_info):
    """Create LINE Flex Message for alert"""
    tz = pytz.timezone('Asia/Bangkok')
    now = datetime.now(tz)
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M')
    
    overall_risk = alert_info['overall_risk']
    
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
    
    # Build alert reasons
    alert_reasons = []
    if alert_info['overall_alert']:
        alert_reasons.append(f"คะแนนรวม {overall_risk}/100 (≥{OVERALL_RISK_THRESHOLD})")
    
    if alert_info['category_alert']:
        for cat_name, score in alert_info['high_risk_categories']:
            info = category_info.get(cat_name, {'name': cat_name.capitalize(), 'emoji': '📌'})
            alert_reasons.append(f"{info['emoji']} {info['name']}: {int(score)} (≥{CATEGORY_RISK_THRESHOLD})")
    
    alert_text = "\n".join([f"• {reason}" for reason in alert_reasons])
    
    # Get all categories
    categories = data.get('categories', {})
    category_items = []
    sorted_cats = sorted(categories.items(), key=lambda x: x[1].get('score', 0), reverse=True)
    
    for cat_key, cat_data in sorted_cats:
        score = cat_data.get('score', 0)
        info = category_info.get(cat_key, {'name': cat_key.capitalize(), 'emoji': '📌'})
        
        # Color based on score
        if score >= 70:
            color = "#EF4444"  # Red
        elif score >= 40:
            color = "#F59E0B"  # Orange
        else:
            color = "#10B981"  # Green
        
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
    
    # Create Flex Message
    flex_message = {
        "type": "flex",
        "altText": f"🚨 RISK ALERT! Overall Risk: {overall_risk}/100",
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
                                "text": "🚨 RISK ALERT",
                                "color": "#FFFFFF",
                                "size": "xl",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": "HIGH",
                                "color": "#FFFFFF",
                                "size": "xs",
                                "align": "end",
                                "gravity": "center"
                            }
                        ]
                    }
                ],
                "backgroundColor": "#DC2626",
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
                                "text": "⚠️ ตรวจพบความเสี่ยงสูง!",
                                "size": "md",
                                "color": "#DC2626",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": alert_text,
                                "size": "sm",
                                "color": "#666666",
                                "wrap": True,
                                "margin": "md"
                            }
                        ],
                        "backgroundColor": "#FEE2E2",
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
                                "color": "#DC2626",
                                "margin": "md"
                            }
                        ],
                        "backgroundColor": "#F3F4F6",
                        "paddingAll": "15px",
                        "cornerRadius": "8px",
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
                                "text": "📈 คะแนนตามหมวด",
                                "size": "md",
                                "weight": "bold",
                                "color": "#1F2937"
                            }
                        ] + category_items,
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
                                "text": f"📅 {date_str} {time_str}",
                                "size": "xs",
                                "color": "#999999"
                            },
                            {
                                "type": "text",
                                "text": "Auto Alert",
                                "size": "xs",
                                "color": "#DC2626",
                                "align": "end",
                                "weight": "bold"
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
                        "color": "#DC2626",
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
        print(f"✅ Alert sent successfully at {datetime.now()}")
        return True
    except Exception as e:
        print(f"❌ Error sending alert: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

def main():
    """Main execution function"""
    print("=" * 50)
    print("Risk29 Alert Checker")
    print("=" * 50)
    
    # Get LINE credentials
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    user_id = os.getenv('LINE_USER_ID')
    
    if not channel_access_token or not user_id:
        print("❌ ERROR: LINE credentials not set")
        return False
    
    # Fetch risk data
    print("📡 Fetching risk data...")
    risk_data = get_risk_data()
    
    if not risk_data:
        print("❌ Failed to fetch risk data")
        return False
    
    print("✅ Risk data fetched")
    
    # Check alert conditions
    print("🔍 Checking alert conditions...")
    alert_info = check_alert_conditions(risk_data)
    
    print(f"Overall Risk: {alert_info['overall_risk']}/100")
    print(f"Overall Alert: {alert_info['overall_alert']}")
    print(f"High Risk Categories: {len(alert_info['high_risk_categories'])}")
    print(f"Should Alert: {alert_info['should_alert']}")
    
    # Load previous state
    state = load_alert_state()
    
    if alert_info['should_alert']:
        # Alert condition met
        if not state.get('alert_active', False):
            # First time alert is triggered
            print("\n🚨 ALERT TRIGGERED! Sending notification...")
            
            flex_message = create_alert_flex_message(risk_data, alert_info)
            success = send_line_message(flex_message, channel_access_token, user_id)
            
            if success:
                # Save state to prevent duplicate alerts
                save_alert_state({
                    'last_alert_sent': datetime.now().isoformat(),
                    'alert_active': True
                })
                print("✅ Alert sent and state saved")
                return True
            else:
                print("❌ Failed to send alert")
                return False
        else:
            print("ℹ️  Alert already active, not sending duplicate")
            return True
    else:
        # No alert condition
        if state.get('alert_active', False):
            print("✅ Risk levels back to normal, clearing alert state")
            save_alert_state({
                'last_alert_sent': state.get('last_alert_sent'),
                'alert_active': False
            })
        else:
            print("✅ No alert needed, risk levels normal")
        return True

if __name__ == "__main__":
    exit(0 if main() else 1)
