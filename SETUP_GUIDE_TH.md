# 🚀 คู่มือติดตั้งแบบเร็ว (5 นาทีเสร็จ!)

## ✅ สิ่งที่คุณต้องมี

1. LINE Notify Token (ที่คุณมีอยู่แล้ว)
2. บัญชี GitHub (สมัครฟรีที่ https://github.com/signup)

## 📝 ขั้นตอนติดตั้ง (5 ขั้นตอน)

### 1️⃣ สร้าง GitHub Repository

1. เข้า https://github.com/new
2. ตั้งชื่อ: `risk29-line-automation`
3. เลือก **Public** ✅
4. กด **Create repository**

### 2️⃣ Upload ไฟล์

**วิธีง่าย (ไม่ต้องใช้ Git):**

1. ดาวน์โหลดไฟล์ทั้งหมดจากโฟลเดอร์นี้ไปเครื่องคุณ
2. ไปที่ Repository ที่สร้างใหม่
3. กด **Add file** → **Upload files**
4. ลากไฟล์ทั้งหมดมาวาง:
   - `send_daily_report.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
5. สร้างโฟลเดอร์ `.github/workflows/` และอัพโหลด `daily-report.yml`
6. กด **Commit changes**

**หรือใช้ Git (ถ้าคุณถนัด):**

```bash
cd /home/ubuntu/risk29-line-automation
git init
git add .
git commit -m "Setup Risk29 LINE automation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/risk29-line-automation.git
git push -u origin main
```

### 3️⃣ ตั้งค่า LINE Token

1. ไปที่ Repository → **Settings** (ขวาบน)
2. เลือก **Secrets and variables** → **Actions**
3. กด **New repository secret**
4. กรอก:
   - **Name**: `LINE_NOTIFY_TOKEN`
   - **Secret**: วาง LINE Token ของคุณ
5. กด **Add secret**

### 4️⃣ เปิดใช้งาน GitHub Actions

1. ไปที่ **Actions** tab
2. กด **I understand my workflows, go ahead and enable them**
3. เลือก workflow **Risk29 Daily Morning Report**
4. กด **Enable workflow**

### 5️⃣ ทดสอบทันที!

1. อยู่ที่ **Actions** tab
2. เลือก **Risk29 Daily Morning Report**
3. กดปุ่ม **Run workflow** (ขวามือ)
4. กด **Run workflow** สีเขียว
5. รอ 30-60 วินาที
6. **เช็ค LINE ของคุณ!** 🎉

## ✨ เสร็จแล้ว!

ตอนนี้ระบบจะส่งรายงานอัตโนมัติทุกเช้า **8:00 น.** (เวลาไทย)

### 📱 ข้อความที่คุณจะได้รับ:

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

## 🔧 การปรับแต่ง

### เปลี่ยนเวลาส่ง

แก้ไขไฟล์ `.github/workflows/daily-report.yml`:

```yaml
schedule:
  # เช้า 7:00 น.
  - cron: '0 0 * * *'
  
  # เช้า 9:00 น.
  - cron: '0 2 * * *'
  
  # ส่งวันละ 2 ครั้ง (เช้า 8:00 + เย็น 18:00)
  - cron: '0 1 * * *'
  - cron: '0 11 * * *'
```

**สูตร**: เวลาไทย - 7 = UTC

### ส่งทุกสัปดาห์แทนทุกวัน

```yaml
schedule:
  # ทุกวันจันทร์ เวลา 8:00 น.
  - cron: '0 1 * * 1'
```

## ❓ แก้ปัญหา

### ไม่ได้รับข้อความ LINE?

1. ✅ เช็คว่า LINE_NOTIFY_TOKEN ตั้งค่าถูกต้อง
2. ✅ ไปดู log ใน Actions tab → คลิก workflow run ล่าสุด
3. ✅ ทดสอบ token ด้วยการ Run workflow ใหม่

### Workflow ไม่ทำงาน?

1. ✅ Repository ต้องเป็น **Public**
2. ✅ Workflow ต้อง **Enable** แล้ว
3. ✅ GitHub Actions อาจมี delay 5-10 นาที

## 💰 ค่าใช้จ่าย

**ฟรี 100%!** ไม่มีค่าใช้จ่ายเลย

- GitHub Actions ให้ Public repo ใช้ฟรีไม่จำกัด
- LINE Notify ฟรี
- ไม่ต้องมี Server
- ไม่ต้องเปิดเครื่องทิ้งไว้

## 🎯 สรุป

✅ ส่งอัตโนมัติทุกเช้า 8:00 น.  
✅ ฟรี 100% ไม่มีค่าใช้จ่าย  
✅ ไม่ต้องมี Backend  
✅ ข้อมูลจริงจาก Dashboard  
✅ ตั้งค่าครั้งเดียว ใช้ได้ตลอด  

**มีปัญหาหรือข้อสงสัย?** ดูคำอธิบายเพิ่มเติมใน `README.md`
