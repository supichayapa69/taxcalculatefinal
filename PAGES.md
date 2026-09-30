# PAGES · แดชบอร์ดความคืบหน้า

กรอกสัปดาห์ที่ 1 แล้วอัปเดตทุกครั้งที่ commit — อาจารย์ดูไฟล์นี้ + `git log` แทนการถาม

**หัวข้อ:** ระบบคำนวณภาษีและงบประมาณตามระเบียบราชการไทย
**data.json เก็บอะไร (field):** id, taxpayer_name, tax_category, sub_type, base_amount, deductions, taxable_base, calculated_tax, effective_rate, status, note
**คัดลอก data.json → data.sample.json แล้ว:** [x]

## team — หน้าทีม (สัปดาห์ 0)
- [x] กรอก `team.json` ครบทุกคน (ชื่อ, รหัส, บทบาท, งานที่รับผิดชอบ)
- [x] เปิด /team เห็นชื่อทุกคน
- [x] commit `team: members filled` + push

## page1 — ผู้รับผิดชอบ: นางสาวสุพิชญา ปะถะมา · แบบจาก catalog: form + list
- [x] คัดลอกจาก catalog แล้วเปลี่ยน TITLE
- [x] ใช้ field ของ data.json ของกลุ่ม
- [x] เปิด /page1 ได้ ไม่มี TODO
- [x] `check.bat` → /page1 ✓ ไม่มี warning
- [x] commit `page1: ภาษีเงินได้บุคคลและนิติบุคคล`

## page2 — ผู้รับผิดชอบ: นางสาวนันท์ภัส พิมพ์ภักดิ์ · แบบจาก catalog: form + list
- [x] คัดลอกจาก catalog แล้วเปลี่ยน TITLE
- [x] ใช้ field ของ data.json ของกลุ่ม
- [x] เปิด /page2 ได้ ไม่มี TODO
- [x] `check.bat` → /page2 ✓ ไม่มี warning
- [x] commit `page2: ภาษีที่ดินและภาษีป้าย`

## page3 — ผู้รับผิดชอบ: นางสาวประภาสินีย์ อิ่นคำ · แบบจาก catalog: stats + search
- [x] คัดลอกจาก catalog แล้วเปลี่ยน TITLE
- [x] ใช้ field ของ data.json ของกลุ่ม
- [x] เปิด /page3 ได้ ไม่มี TODO
- [x] `check.bat` → /page3 ✓ ไม่มี warning
- [x] commit `page3: สรุปงบประมาณและสถิติภาษี`

## models.py — ผู้รับผิดชอบ: นางสาวประภาสินีย์ อิ่นคำ
- [x] เปลี่ยนชื่อ class ให้ตรงหัวข้อ (TaxRecord), field ตรง data.json
- [x] method 1 ตัวที่มีประโยชน์ (describe, get_effective_rate, to_dict ไม่เหลือ TODO)
- [x] มีหน้าใดหน้าหนึ่งใช้ class นี้ (page3.py เรียกใช้ TaxRecord และเมธอด)
- [x] `python check_project.py` → class ✓ 9/9
- [x] commit `models: TaxRecord`

## ส่งงาน
- [x] `check.bat` → 60/60, pytest 4 passed, ไม่มี warning
- [ ] ทุกคนอยู่ใน `git log`
- [ ] นำเสนอ: ทุกคนอธิบายหน้าของตัวเอง 1 นาที
