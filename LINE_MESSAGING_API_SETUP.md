# 🔧 วิธีตั้งค่า LINE Messaging API (แบบละเอียด)

LINE Notify จะหยุดให้บริการ 31 มีนาคม 2568 ดังนั้นเราจะใช้ **LINE Messaging API** แทน ซึ่งดีกว่าและไม่มีวันหมดอายุ

---

## 📋 สิ่งที่ต้องเตรียม

1. บัญชี LINE (ที่จะรับข้อความ)
2. อีเมล (สำหรับสมัคร LINE Developers)
3. เวลาประมาณ 10-15 นาที

---

## 🚀 ขั้นตอนที่ 1: สมัคร LINE Developers

### 1.1 เปิดหน้าสมัคร
1. เปิดเบราว์เซอร์ไปที่ https://developers.line.biz/console/
2. กดปุ่ม **Log in** (มุมขวาบน)

### 1.2 ล็อกอิน LINE
1. ล็อกอินด้วย LINE account ของคุณ
   - ใส่อีเมลและรหัสผ่าน หรือ
   - สแกน QR Code ด้วยมือถือ
2. กด **Log in**

### 1.3 ยอมรับข้อตกลง
1. อ่านข้อตกลงการใช้งาน
2. ติ๊กถูก **I agree to the LINE Developers Agreement**
3. กด **Agree**

✅ **เสร็จแล้ว!** ตอนนี้คุณเข้าสู่ LINE Developers Console แล้ว

---

## 📦 ขั้นตอนที่ 2: สร้าง Provider

Provider คือกลุ่มของ Channel (เหมือนโฟลเดอร์)

### 2.1 สร้าง Provider ใหม่
1. ในหน้า Console กดปุ่ม **Create** (หรือ **Create a new provider**)
2. กรอกข้อมูล:
   - **Provider name**: `Risk29` (หรือชื่ออะไรก็ได้)
3. กดปุ่ม **Create**

✅ **เสร็จแล้ว!** ตอนนี้คุณมี Provider แล้ว

---

## 📡 ขั้นตอนที่ 3: สร้าง Messaging API Channel

### 3.1 สร้าง Channel ใหม่
1. ในหน้า Provider กดปุ่ม **Create a Messaging API channel**
2. กรอกข้อมูลดังนี้:

#### Channel type
- เลือก: **Messaging API** (เลือกอยู่แล้ว)

#### Provider
- เลือก: **Risk29** (หรือ Provider ที่สร้างไว้)

#### Channel icon (ไม่บังคับ)
- อัพโหลดรูปไอคอน หรือข้ามไปก็ได้

#### Channel name
- พิมพ์: `Risk29 Daily Report`

#### Channel description
- พิมพ์: `Automated daily risk summary reports`

#### Category
- เลือก: **Finance** หรือ **News**

#### Subcategory
- เลือกตามที่เหมาะสม

#### Email address
- ใส่อีเมลของคุณ

### 3.2 ยอมรับข้อตกลง
1. อ่านข้อตกลง
2. ติ๊กถูกทั้งหมด:
   - ✅ LINE Official Account Terms of Use
   - ✅ LINE Official Account API Terms of Use
3. กดปุ่ม **Create** (ด้านล่าง)

✅ **เสร็จแล้ว!** ตอนนี้คุณมี Messaging API Channel แล้ว

---

## 🔑 ขั้นตอนที่ 4: ดึง Channel Access Token

### 4.1 เข้าสู่หน้า Channel
1. กดที่ Channel ที่เพิ่งสร้าง (`Risk29 Daily Report`)
2. กดแท็บ **Messaging API** (ด้านบน)

### 4.2 สร้าง Channel Access Token
1. เลื่อนลงมาหาส่วน **Channel access token**
2. กดปุ่ม **Issue** (ถ้ายังไม่มี token)
   - หรือถ้ามีแล้ว จะเห็น token ยาวๆ
3. **คัดลอก Token**
   - กดปุ่ม Copy หรือ
   - เลือกทั้งหมดแล้วกด Ctrl+C / Cmd+C

⚠️ **สำคัญ**: เก็บ Token นี้ไว้ดีๆ จะใช้ในขั้นตอนที่ 6

**ตัวอย่าง Token**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
- ยาวมาก (100+ ตัวอักษร)
- เริ่มต้นด้วย `eyJ` หรือตัวอักษรอื่น

✅ **เสร็จแล้ว!** ได้ Channel Access Token แล้ว

---

## 👤 ขั้นตอนที่ 5: หา LINE User ID ของคุณ

### วิธีที่ 1: ใช้ LINE Official Account Manager (แนะนำ)

#### 5.1 เปิด LINE Official Account Manager
1. ไปที่ https://manager.line.biz/
2. ล็อกอินด้วย LINE account เดียวกัน

#### 5.2 เลือก Account
1. เลือก Official Account ที่เพิ่งสร้าง (`Risk29 Daily Report`)

#### 5.3 เพิ่มเพื่อนกับ Bot
1. ในหน้า Manager จะเห็น QR Code หรือลิงก์เพิ่มเพื่อน
2. **เปิด LINE บนมือถือ**
3. สแกน QR Code หรือกดลิงก์เพิ่มเพื่อน
4. กดปุ่ม **เพิ่ม** (Add)

✅ **เสร็จแล้ว!** ตอนนี้คุณเป็นเพื่อนกับ Bot แล้ว

#### 5.4 หา User ID

**วิธีที่ 1: ใช้ LINE Bot (ง่ายที่สุด)**

1. ส่งข้อความอะไรก็ได้ไปยัง Bot (เช่น "Hello")
2. ไปที่ LINE Developers Console → Channel → **Messaging API** tab
3. เลื่อนลงมาหา **Webhook URL**
4. กดปุ่ม **Verify** (ถ้ามี)

**หรือวิธีที่ 2: ใช้ LINE Bot SDK**

สร้างไฟล์ `get_user_id.py`:

```python
from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    body = request.get_json()
    print("Received webhook:")
    print(body)
    
    # แสดง User ID
    if 'events' in body:
        for event in body['events']:
            if 'source' in event and 'userId' in event['source']:
                user_id = event['source']['userId']
                print(f"\n✅ YOUR USER ID: {user_id}\n")
    
    return 'OK'

if __name__ == "__main__":
    app.run(port=5000)
```

รันแล้วส่งข้อความไปยัง Bot จะเห็น User ID ใน console

**วิธีที่ 3: ใช้ Webhook URL (ง่ายกว่า)**

1. ไปที่ https://webhook.site/
2. คัดลอก URL ที่ได้ (เช่น `https://webhook.site/abc123...`)
3. กลับไปที่ LINE Developers Console → **Messaging API** tab
4. เลื่อนลงมาหา **Webhook settings**
5. กดปุ่ม **Edit** ที่ Webhook URL
6. วาง URL จาก webhook.site
7. กดปุ่ม **Update**
8. เปิด **Use webhook** (เป็น ON)
9. **ส่งข้อความอะไรก็ได้ไปยัง Bot บนมือถือ**
10. กลับไปที่ webhook.site
11. คุณจะเห็น request เข้ามา
12. ดูใน JSON จะเห็น `"userId": "U1234567890abcdef..."`
13. **คัดลอก User ID นี้**

⚠️ **สำคัญ**: เก็บ User ID นี้ไว้ดีๆ จะใช้ในขั้นตอนที่ 6

**ตัวอย่าง User ID**:
```
U1234567890abcdef1234567890abcdef
```
- เริ่มต้นด้วย `U`
- ตามด้วยตัวอักษรและตัวเลข 32 ตัว

✅ **เสร็จแล้ว!** ได้ User ID แล้ว

---

## 🔐 ขั้นตอนที่ 6: ตั้งค่า GitHub Secrets

ตอนนี้คุณมี 2 ค่าที่ต้องใส่:
1. **LINE_CHANNEL_ACCESS_TOKEN** (จากขั้นตอนที่ 4)
2. **LINE_USER_ID** (จากขั้นตอนที่ 5)

### 6.1 เข้าสู่หน้า GitHub Secrets
1. ไปที่ Repository: https://github.com/minetose-oss/risk29-line-automation
2. กดแท็บ **Settings** (มุมขวาบน)
3. เลือก **Secrets and variables** → **Actions** (ทางซ้าย)

### 6.2 เพิ่ม Secret ที่ 1: LINE_CHANNEL_ACCESS_TOKEN
1. กดปุ่ม **New repository secret**
2. กรอก:
   - **Name**: `LINE_CHANNEL_ACCESS_TOKEN`
   - **Secret**: วาง Channel Access Token ที่คัดลอกไว้
3. กดปุ่ม **Add secret**

### 6.3 เพิ่ม Secret ที่ 2: LINE_USER_ID
1. กดปุ่ม **New repository secret** อีกครั้ง
2. กรอก:
   - **Name**: `LINE_USER_ID`
   - **Secret**: วาง User ID ที่คัดลอกไว้
3. กดปุ่ม **Add secret**

### 6.4 ตรวจสอบ
- คุณจะเห็น 2 Secrets:
  - ✅ `LINE_CHANNEL_ACCESS_TOKEN`
  - ✅ `LINE_USER_ID`

✅ **เสร็จแล้ว!** GitHub รู้จัก LINE credentials แล้ว

---

## 🧪 ขั้นตอนที่ 7: ทดสอบส่งข้อความ

### 7.1 เข้าสู่หน้า Actions
1. ไปที่ Repository
2. กดแท็บ **Actions** (ด้านบน)

### 7.2 รัน Workflow
1. กดที่ **Risk29 Daily Morning Report** (ทางซ้าย)
2. กดปุ่ม **Run workflow** (ขวามือ)
3. เลือก **Branch: main**
4. กดปุ่ม **Run workflow** (สีเขียว)

### 7.3 รอผลลัพธ์
1. รอ 30-60 วินาที
2. รีเฟรชหน้า (F5)
3. กดที่ workflow run ที่เพิ่งสร้าง
4. กดที่ **send-report**
5. ดู log

### 7.4 เช็ค LINE
- **เปิด LINE บนมือถือ**
- เปิดแชทกับ Bot (`Risk29 Daily Report`)
- คุณจะได้รับข้อความ:

```
🎯 Risk29 Morning Summary
📅 2025-10-31 21:30

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

✅ **สำเร็จ!** ถ้าได้รับข้อความ แสดงว่าทุกอย่างทำงานแล้ว!

---

## ⏰ ขั้นตอนที่ 8: ตั้งเวลาอัตโนมัติ

ระบบจะส่งอัตโนมัติทุกเช้า 8:00 น. (GMT+7) แล้ว ไม่ต้องทำอะไรเพิ่ม!

- **เวลา**: ทุกวัน 8:00 น. (เวลาไทย)
- **ความถี่**: ทุกวัน (รวมวันหยุด)

---

## 🎯 สรุป

ตอนนี้คุณมีระบบที่:

✅ ใช้ LINE Messaging API (ไม่มีวันหมดอายุ)  
✅ ส่งอัตโนมัติทุกเช้า 8:00 น.  
✅ ฟรี 100% (GitHub Actions)  
✅ ไม่ต้องมี Backend Server  
✅ ข้อมูลจริงจาก Dashboard  

**เพลิดเพลินกับการรับรายงานทุกเช้า! 🎉**

---

## 🔧 แก้ปัญหา

### ปัญหา: ไม่ได้รับข้อความ

1. ✅ ตรวจสอบว่าเพิ่มเพื่อนกับ Bot แล้ว
2. ✅ ตรวจสอบ LINE_CHANNEL_ACCESS_TOKEN ถูกต้อง
3. ✅ ตรวจสอบ LINE_USER_ID ถูกต้อง
4. ✅ ดู log ใน GitHub Actions ว่ามี error อะไร

### ปัญหา: Error "Invalid access token"

- ❌ Channel Access Token ผิด
- ✅ ไปที่ LINE Developers Console → Channel → Messaging API
- ✅ Issue token ใหม่
- ✅ อัพเดทใน GitHub Secrets

### ปัญหา: Error "Invalid user ID"

- ❌ User ID ผิด
- ✅ ใช้ webhook.site หา User ID ใหม่
- ✅ อัพเดทใน GitHub Secrets

---

## 📞 ต้องการความช่วยเหลือ?

ถ้าติดปัญหาตรงไหน บอกผมได้เลยครับ! 😊
