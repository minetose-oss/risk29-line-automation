# ✅ สรุปโซลูชัน: LINE Notification อัตโนมัติ (ฟรี 100%)

## 🎯 สิ่งที่ได้

ระบบส่ง LINE notification อัตโนมัติที่:

✅ **ส่งอัตโนมัติทุกเช้า 8:00 น.** (เวลาไทย GMT+7)  
✅ **ฟรี 100%** ไม่มีค่าใช้จ่ายเลย (ใช้ GitHub Actions ฟรี)  
✅ **ไม่ต้องมี Backend Server** (ไม่ต้อง upgrade dashboard)  
✅ **ดึงข้อมูลจริงจาก Dashboard** (https://riskdash-h38zfvrd.manus.space)  
✅ **ทำงานตลอด 24/7** (ไม่ต้องเปิดเครื่องทิ้งไว้)  

## 📱 ตัวอย่างข้อความที่จะได้รับ

```
🎯 Risk29 Morning Summary
📅 2025-10-31 08:00

📊 Overall Risk Score: 18.5/100

⚠️ Top Risk Categories:
• 💧 Liquidity: 50
• 📊 Valuation: 48
• 🌍 Macro: 24

📈 Signal Summary:
• High Risk: 0 signals
• Medium Risk: 0 signals
• Low Risk: 25 signals

Total Signals Analyzed: 25

✅ Pipeline executed successfully
```

## 🔧 เทคโนโลยีที่ใช้

1. **Python Script** (`send_daily_report.py`)
   - ดึงข้อมูลจาก Dashboard (risk_data.json)
   - คำนวณ Overall Risk Score
   - หา Top 3 Risk Categories
   - นับ Signals แยกตามระดับความเสี่ยง
   - ส่งข้อความผ่าน LINE Notify API

2. **GitHub Actions** (`.github/workflows/daily-report.yml`)
   - ตั้งเวลาส่งอัตโนมัติด้วย cron: `0 1 * * *` (8:00 AM GMT+7)
   - รัน Python script ทุกวัน
   - ฟรีไม่จำกัดสำหรับ Public repositories

3. **LINE Notify API**
   - ส่งข้อความไปยัง LINE ของคุณ
   - ใช้ Token ที่คุณมีอยู่แล้ว
   - ฟรี ไม่มีค่าใช้จ่าย

## 📂 ไฟล์ที่สำคัญ

```
risk29-line-automation/
├── send_daily_report.py          # Python script หลัก
├── requirements.txt               # Python dependencies
├── .github/workflows/
│   └── daily-report.yml          # GitHub Actions workflow
├── README.md                      # คู่มือใช้งานแบบละเอียด (ภาษาอังกฤษ)
├── SETUP_GUIDE_TH.md             # คู่มือติดตั้งแบบเร็ว (ภาษาไทย)
├── test_demo.py                   # สคริปต์ทดสอบ (ไม่ส่ง LINE จริง)
└── .gitignore                     # Git ignore file
```

## 🚀 วิธีติดตั้ง (5 ขั้นตอน)

### 1. สร้าง GitHub Repository
- ไป https://github.com/new
- ตั้งชื่อ: `risk29-line-automation`
- เลือก **Public**
- กด Create repository

### 2. Upload ไฟล์
- ดาวน์โหลดไฟล์ทั้งหมดจาก zip
- Upload ไปยัง GitHub Repository
- หรือใช้ Git push

### 3. ตั้งค่า LINE Token
- ไปที่ Settings → Secrets and variables → Actions
- เพิ่ม Secret: `LINE_NOTIFY_TOKEN`
- วาง LINE Token ของคุณ

### 4. เปิดใช้งาน GitHub Actions
- ไปที่ Actions tab
- Enable workflow

### 5. ทดสอบทันที
- กด Run workflow
- เช็ค LINE ของคุณ

**รายละเอียดเพิ่มเติม**: อ่าน `SETUP_GUIDE_TH.md`

## ⏰ กำหนดการทำงาน

- **เวลา**: ทุกวัน 8:00 น. (GMT+7)
- **Cron**: `0 1 * * *` (1:00 AM UTC)
- **ความถี่**: ทุกวัน (รวมวันหยุด)

### เปลี่ยนเวลาส่ง

แก้ไข `.github/workflows/daily-report.yml`:

```yaml
schedule:
  # เช้า 7:00 น.
  - cron: '0 0 * * *'
  
  # เช้า 9:00 น.
  - cron: '0 2 * * *'
  
  # ส่งวันละ 2 ครั้ง
  - cron: '0 1 * * *'   # 8:00 AM
  - cron: '0 11 * * *'  # 6:00 PM
```

**สูตรคำนวณ**: เวลาไทย - 7 = UTC

## 💰 ค่าใช้จ่าย

**ฟรี 100%!**

- ✅ GitHub Actions: ฟรีไม่จำกัดสำหรับ Public repo
- ✅ LINE Notify: ฟรี
- ✅ ไม่ต้องมี Server
- ✅ ไม่ต้อง upgrade Dashboard

สคริปต์ใช้เวลาประมาณ 30 วินาที/ครั้ง = 15 นาที/เดือน

## 🧪 การทดสอบ

### ทดสอบบนเครื่องตัวเอง (ไม่ส่ง LINE จริง)

```bash
cd risk29-line-automation
pip install -r requirements.txt
python3 test_demo.py
```

จะแสดงข้อความที่จะส่งไปยัง LINE (ไม่ส่งจริง)

### ทดสอบส่ง LINE จริง

```bash
export LINE_NOTIFY_TOKEN="your_token_here"
python3 send_daily_report.py
```

### ทดสอบบน GitHub Actions

1. ไปที่ Actions tab
2. เลือก workflow "Risk29 Daily Morning Report"
3. กด Run workflow
4. เช็ค LINE ของคุณ

## 📊 ข้อมูลที่แสดง

1. **Overall Risk Score**: คะแนนความเสี่ยงรวม (0-100)
2. **Top 3 Risk Categories**: หมวดที่มีความเสี่ยงสูงสุด 3 อันดับแรก
3. **Signal Summary**: จำนวน signals แยกตามระดับ
   - High Risk (≥70)
   - Medium Risk (40-69)
   - Low Risk (<40)
4. **Total Signals**: จำนวน signals ทั้งหมดที่วิเคราะห์

## 🔧 การปรับแต่ง

### เปลี่ยนจำนวน Top Categories

แก้ไข `send_daily_report.py`:

```python
# แสดง Top 5 แทน Top 3
top_categories = get_top_risk_categories(data, top_n=5)
```

### เปลี่ยนเกณฑ์ความเสี่ยง

แก้ไข `count_signals_by_risk()`:

```python
if score >= 80:      # เดิม 70
    high_count += 1
elif score >= 50:    # เดิม 40
    medium_count += 1
```

### เพิ่มข้อมูลเพิ่มเติม

แก้ไข `format_message()` เพื่อเพิ่มข้อมูลที่ต้องการ

## ❓ แก้ปัญหา

### ไม่ได้รับข้อความ LINE

1. ✅ เช็ค LINE_NOTIFY_TOKEN ใน GitHub Secrets
2. ✅ ดู log ใน Actions tab
3. ✅ ทดสอบ token ด้วย curl:
   ```bash
   curl -X POST https://notify-api.line.me/api/notify \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d "message=Test"
   ```

### Workflow ไม่ทำงาน

1. ✅ Repository ต้องเป็น **Public**
2. ✅ Workflow ต้อง **Enable** แล้ว
3. ✅ อาจมี delay 5-10 นาที

### ดึงข้อมูลไม่ได้

1. ✅ เช็คว่า Dashboard ยังทำงานอยู่
2. ✅ เช็คว่า risk_data.json accessible
3. ✅ ดู error ใน log

## 📝 ข้อจำกัด

- Dashboard ต้องยังทำงานอยู่ (ไม่ถูก unpublish)
- ข้อมูลดึงจาก `risk_data.json` ที่ Dashboard
- ถ้า Dashboard ปิด script จะไม่สามารถดึงข้อมูลได้
- LINE Notify Token ต้องยังใช้งานได้

## 🎯 สรุป

ตอนนี้คุณมีระบบที่:

✅ ส่งรายงานอัตโนมัติทุกเช้า 8:00 น.  
✅ ฟรี 100% ไม่มีค่าใช้จ่าย  
✅ ไม่ต้องมี Backend Server  
✅ ไม่ต้องเปิดเครื่องทิ้งไว้  
✅ ข้อมูลจริงจาก Dashboard  
✅ ตั้งค่าครั้งเดียว ใช้ได้ตลอด  

**เพลิดเพลินกับการรับรายงานทุกเช้า! 🎉**

---

## 📞 ติดต่อ & ช่วยเหลือ

- **คู่มือติดตั้งแบบเร็ว**: `SETUP_GUIDE_TH.md`
- **คู่มือแบบละเอียด**: `README.md`
- **ทดสอบข้อความ**: รัน `python3 test_demo.py`
- **ส่งข้อความจริง**: รัน `python3 send_daily_report.py`

มีปัญหาหรือข้อสงสัย? อ่านคู่มือใน README.md หรือ SETUP_GUIDE_TH.md
