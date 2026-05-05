# /check-inbox

> อ่านข้อความใหม่จาก inbox

## Behavior

1. อ่านไฟล์ทั้งหมดใน `ψ/inbox/` เรียงตามวันที่
2. แสดงข้อความที่ยังไม่ได้อ่าน (ไฟล์ที่ยังไม่ได้ย้ายไป archive)
3. หลังอ่านแล้ว ถาม: "ย้ายไป archive ไหม?"
4. ถ้าใช่ — ย้ายไป `ψ/archive/inbox/`

## Auto-trigger

เรียกอัตโนมัติเมื่อเริ่ม session ใหม่ (ใส่ใน /recap flow).

## Reply

ถ้าต้องการตอบกลับ:
- เขียนไฟล์ไปที่ inbox ของผู้รับ
- IZU inbox: `D:/Claude/izu-oracle/ψ/inbox/`
- ใช้ format: `YYYYMMDD_HHMM_from_bt.md`

## Format

```
📬 Inbox (N ข้อความใหม่)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 [filename]
From: [sender]
Date: [date]

[content preview - first 5 lines]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
