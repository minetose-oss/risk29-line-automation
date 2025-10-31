# Risk29 Daily Morning Report - LINE Notification Automation

ระบบส่งรายงานสรุปความเสี่ยงทางการเงินอัตโนมัติทุกเช้า 8:00 น. (GMT+7) ผ่าน LINE Notify

## 🎯 คุณสมบัติ

- ✅ ส่งรายงานอัตโนมัติทุกวันเวลา 8:00 น. (เวลาไทย)
- ✅ แสดง Overall Risk Score
- ✅ แสดง Top 3 Risk Categories
- ✅ สรุปจำนวน Signals แยกตามระดับความเสี่ยง (High/Medium/Low)
- ✅ ใช้ GitHub Actions ฟรี 100% (ไม่มีค่าใช้จ่าย)
- ✅ ดึงข้อมูลจาก Dashboard จริง (https://riskdash-h38zfvrd.manus.space)

## 📋 ตัวอย่างข้อความที่ส่ง

```
🎯 Risk29 Morning Summary
📅 2025-10-31 08:00

📊 Overall Risk Score: 67.5/100

⚠️ Top Risk Categories:
• 📊 Valuation: 85
• 💧 Liquidity: 72
• 💳 Credit: 68

📈 Signal Summary:
• High Risk: 8 signals
• Medium Risk: 12 signals
• Low Risk: 5 signals

Total Signals Analyzed: 25

✅ Pipeline executed successfully
```

## 🚀 วิธีติดตั้ง (Setup)

### ขั้นตอนที่ 1: สร้าง GitHub Repository

1. ไปที่ https://github.com/new
2. ตั้งชื่อ Repository เช่น `risk29-line-automation`
3. เลือก **Public** (จำเป็นสำหรับ GitHub Actions ฟรี)
4. คลิก "Create repository"

### ขั้นตอนที่ 2: Upload โค้ดไปยัง GitHub

**วิธีที่ 1: ใช้ GitHub Web Interface (ง่ายที่สุด)**

1. ไปที่ Repository ที่สร้างใหม่
2. คลิก "uploading an existing file"
3. ลากไฟล์ทั้งหมดจากโฟลเดอร์นี้ไปวาง:
   - `send_daily_report.py`
   - `requirements.txt`
   - `.github/workflows/daily-report.yml` (สร้างโฟลเดอร์ด้วย)
4. คลิก "Commit changes"

**วิธีที่ 2: ใช้ Git Command Line**

```bash
cd /home/ubuntu/risk29-line-automation
git init
git add .
git commit -m "Initial commit: Risk29 LINE automation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/risk29-line-automation.git
git push -u origin main
```

### ขั้นตอนที่ 3: ตั้งค่า LINE Notify Token

1. ไปที่ Repository → **Settings** → **Secrets and variables** → **Actions**
2. คลิก **New repository secret**
3. ตั้งค่า:
   - Name: `LINE_NOTIFY_TOKEN`
   - Secret: วาง LINE Notify Token ของคุณ
4. คลิก **Add secret**

### ขั้นตอนที่ 4: เปิดใช้งาน GitHub Actions

1. ไปที่ Repository → **Actions** tab
2. คลิก "I understand my workflows, go ahead and enable them"
3. คลิก workflow "Risk29 Daily Morning Report"
4. คลิก "Enable workflow"

### ขั้นตอนที่ 5: ทดสอบทันที (ไม่ต้องรอถึง 8 โมงเช้า)

1. ไปที่ **Actions** tab
2. คลิก workflow "Risk29 Daily Morning Report"
3. คลิกปุ่ม **Run workflow** ทางขวามือ
4. คลิก **Run workflow** สีเขียว
5. รอ 30-60 วินาที แล้วเช็ค LINE ของคุณ

## ⏰ กำหนดการส่งอัตโนมัติ

- **เวลา**: ทุกวันเวลา 8:00 น. (GMT+7 / เวลาไทย)
- **Cron**: `0 1 * * *` (1:00 AM UTC = 8:00 AM GMT+7)
- **ความถี่**: ทุกวัน รวมวันหยุด

### เปลี่ยนเวลาส่ง

แก้ไขไฟล์ `.github/workflows/daily-report.yml`:

```yaml
schedule:
  # เช้า 7:00 น. (GMT+7)
  - cron: '0 0 * * *'
  
  # เช้า 9:00 น. (GMT+7)
  - cron: '0 2 * * *'
  
  # ส่งวันละ 2 ครั้ง: เช้า 8:00 และเย็น 18:00
  - cron: '0 1 * * *'   # 8:00 AM
  - cron: '0 11 * * *'  # 6:00 PM
```

**สูตรคำนวณ**: เวลาไทย - 7 ชั่วโมง = UTC

## 🧪 การทดสอบ

### ทดสอบบนเครื่องตัวเอง

```bash
# ติดตั้ง dependencies
pip install -r requirements.txt

# ตั้งค่า LINE token
export LINE_NOTIFY_TOKEN="your_token_here"

# รันสคริปต์
python send_daily_report.py
```

### ทดสอบบน GitHub Actions

1. ไปที่ **Actions** tab
2. เลือก workflow "Risk29 Daily Morning Report"
3. คลิก **Run workflow**
4. เช็ค LINE ของคุณภายใน 1 นาที

## 📊 ตรวจสอบสถานะ

### ดู Log การทำงาน

1. ไปที่ **Actions** tab
2. คลิกที่ workflow run ล่าสุด
3. คลิก job "send-report"
4. ดู log แต่ละ step

### ตรวจสอบว่าทำงานหรือไม่

- ✅ ถ้าเห็น "✅ LINE notification sent successfully" = ส่งสำเร็จ
- ❌ ถ้าเห็น "❌ Error" = มีปัญหา (เช็ค token หรือ network)

## 🔧 แก้ไขปัญหา

### ปัญหา: ไม่ได้รับข้อความ LINE

1. เช็คว่า LINE_NOTIFY_TOKEN ตั้งค่าถูกต้องใน GitHub Secrets
2. เช็คว่า workflow ทำงานจริงใน Actions tab
3. ดู log ว่ามี error อะไร
4. ทดสอบ token ด้วย curl:
   ```bash
   curl -X POST https://notify-api.line.me/api/notify \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d "message=Test"
   ```

### ปัญหา: Workflow ไม่ทำงานอัตโนมัติ

1. เช็คว่า Repository เป็น **Public** (GitHub Actions ฟรีสำหรับ Public repo)
2. เช็คว่า workflow ถูก **Enable** แล้ว
3. GitHub Actions อาจมี delay 5-10 นาที จากเวลาที่กำหนด

### ปัญหา: ดึงข้อมูลไม่ได้

1. เช็คว่า Dashboard ยังทำงานอยู่: https://riskdash-h38zfvrd.manus.space
2. เช็คว่าไฟล์ `risk_data.json` accessible
3. ดู error ใน log

## 💰 ค่าใช้จ่าย

**ฟรี 100%!** 

GitHub Actions ให้:
- Public repositories: **Unlimited minutes ฟรี**
- Private repositories: 2,000 minutes/เดือน ฟรี

สคริปต์นี้ใช้เวลาประมาณ 30 วินาทีต่อครั้ง = 15 นาที/เดือน

## 📝 หมายเหตุ

- Dashboard ต้องยังทำงานอยู่ (ไม่ถูก unpublish)
- ข้อมูลดึงจาก `risk_data.json` ที่ Dashboard
- ถ้า Dashboard ปิด script จะส่ง error notification
- LINE Notify Token ไม่มีวันหมดอายุ (ยกเว้นถูก revoke)

## 🎉 สรุป

ตอนนี้คุณมีระบบส่งรายงานอัตโนมัติที่:
- ✅ ทำงานทุกวันเวลา 8:00 น. เวลาไทย
- ✅ ไม่มีค่าใช้จ่าย (ใช้ GitHub Actions ฟรี)
- ✅ ไม่ต้องมี Backend Server
- ✅ ไม่ต้องเปิดเครื่องทิ้งไว้
- ✅ ส่งข้อมูลจริงจาก Dashboard

**เพลิดเพลินกับการรับรายงานทุกเช้า! 🎯**
