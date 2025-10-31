# 🎯 Risk29 LINE Automation

Automated daily risk summary reports and real-time alerts via LINE Messaging API.

## 📋 Features

### 1. 📅 Daily Morning Report (8:00 AM GMT+7)
- Beautiful dashboard-style Flex Message
- Overall risk score with color-coded indicators
- Category breakdown with emojis
- Top 3 highest risk categories
- Interactive button to view full dashboard

### 2. 🚨 Real-Time Risk Alerts (Every 30 minutes)
- Automatic monitoring of risk levels
- Sends alert when:
  - Overall Risk Score ≥ 60, OR
  - Any category score ≥ 70
- Smart alert system (no duplicate alerts)
- Red-themed urgent alert message

## 🚀 Setup

### Prerequisites
- LINE Messaging API Channel
- GitHub Account
- 10-15 minutes

### Quick Start

1. **Set up LINE Messaging API** (see `LINE_MESSAGING_API_SETUP.md`)
2. **Repository already created**: https://github.com/minetose-oss/risk29-line-automation
3. **GitHub Secrets already configured**:
   - ✅ `LINE_CHANNEL_ACCESS_TOKEN`
   - ✅ `LINE_USER_ID`
4. **GitHub Actions enabled**
5. Done! You'll receive automated reports and alerts

## 📊 What You'll Receive

### Daily Report (8:00 AM)
Beautiful dashboard card with:
- 📊 Overall risk score (color-coded)
- 📈 All category scores with emojis
- ⚠️ Top 3 highest risks
- 🔘 Button to view full dashboard

### Risk Alert (When triggered)
Urgent red alert card with:
- 🚨 Alert header
- ⚠️ Specific reasons for alert
- 📊 Current risk scores
- 🔘 Button to view dashboard

## ⚙️ Configuration

### Change Daily Report Time
Edit `.github/workflows/daily-report.yml`:
```yaml
schedule:
  - cron: '0 1 * * *'  # 8:00 AM GMT+7 (1:00 AM UTC)
```

### Change Alert Frequency
Edit `.github/workflows/alert-checker.yml`:
```yaml
schedule:
  - cron: '*/30 * * * *'  # Every 30 minutes
```

### Adjust Alert Thresholds
Edit `check_and_alert.py`:
```python
OVERALL_RISK_THRESHOLD = 60  # Overall risk alert threshold
CATEGORY_RISK_THRESHOLD = 70  # Category risk alert threshold
```

## 📁 File Structure

```
.
├── send_daily_report.py       # Daily morning report script
├── check_and_alert.py          # Alert checker script
├── requirements.txt            # Python dependencies
├── .github/
│   └── workflows/
│       ├── daily-report.yml    # Daily report schedule
│       └── alert-checker.yml   # Alert checker schedule
├── README.md                   # This file
├── LINE_MESSAGING_API_SETUP.md # Detailed setup guide
└── SETUP_GUIDE_TH.md          # Quick setup guide (Thai)
```

## 🔧 How It Works

### Daily Report Flow
1. GitHub Actions triggers at 8:00 AM GMT+7
2. Script fetches data from dashboard
3. Creates beautiful Flex Message
4. Sends to your LINE account

### Alert Flow
1. GitHub Actions runs every 30 minutes
2. Script checks current risk levels
3. If threshold exceeded:
   - Creates urgent alert message
   - Sends to your LINE account
   - Saves alert state
4. If risk returns to normal:
   - Clears alert state
   - Ready for next alert

### Smart Alert System
- **No Duplicate Alerts**: Only sends once when threshold is first exceeded
- **Auto Recovery**: Clears alert state when risk returns to normal
- **Persistent State**: Remembers alert status across runs (using /tmp file)

## 💰 Cost

**100% FREE!**
- ✅ LINE Messaging API: Free
- ✅ GitHub Actions: Free for public repos (unlimited minutes)
- ✅ No server required
- ✅ No maintenance cost

## 🎨 Customization

### Change Colors
Edit the color codes in `send_daily_report.py` and `check_and_alert.py`:
```python
"#1E40AF"  # Blue header
"#10B981"  # Green (low risk)
"#F59E0B"  # Orange (medium risk)
"#EF4444"  # Red (high risk)
```

### Change Alert Thresholds
```python
OVERALL_RISK_THRESHOLD = 60   # Change to 50, 70, etc.
CATEGORY_RISK_THRESHOLD = 70  # Change to 60, 80, etc.
```

### Add More Data
Extend the Flex Message structure in the scripts to include:
- Signal details
- Historical trends
- Custom metrics

## 🧪 Testing

### Test Daily Report
1. Go to Actions → Risk29 Daily Morning Report
2. Click "Run workflow"
3. Check your LINE

### Test Alert System
1. Go to Actions → Risk29 Alert Checker
2. Click "Run workflow"
3. Check your LINE (only if thresholds exceeded)

### Manual Testing
```bash
# Set environment variables
export LINE_CHANNEL_ACCESS_TOKEN="your_token"
export LINE_USER_ID="your_user_id"

# Test daily report
python send_daily_report.py

# Test alert checker
python check_and_alert.py
```

## 🔍 Monitoring

### View Workflow Runs
- Go to Actions tab
- See all past runs and their status
- Click on any run to see detailed logs

### Check Alert State
The alert system saves state to prevent duplicates:
- File: `/tmp/risk29_alert_state.json`
- Contains: last alert time and active status
- Auto-clears when risk returns to normal

## 📞 Support

For issues or questions:
1. Check `LINE_MESSAGING_API_SETUP.md` for setup help
2. Review GitHub Actions logs for errors
3. Verify LINE credentials in Secrets

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Credits

- Dashboard: Risk29 Financial Risk Monitor
- Powered by: LINE Messaging API + GitHub Actions
- Built with: Python + LINE Flex Message

---

**Enjoy your automated risk monitoring! 🎉**
