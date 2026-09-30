"""pages/page3.py — สรุปงบประมาณและสถิติภาษี (Analytics & Statistics)
ผู้รับผิดชอบ: นางสาวประภาสินีย์ อิ่นคำ (รหัสนักศึกษา 69130840342)
"""
import models
import storage

TITLE = "สรุปงบประมาณและสถิติภาษี"


def build(query=None):
    """วิเคราะห์และประมวลผลข้อมูลภาษีทั้งหมด โดยใช้ TaxRecord จาก models.py"""
    query = query or {}
    search_keyword = query.get("q", "").strip().lower()
    filter_category = query.get("cat", "").strip()

    items = storage.load()

    # สร้างออบเจกต์ TaxRecord จาก models.py
    tax_objects = []
    for it in items:
        record = models.TaxRecord(
            taxpayer_name=it.get("taxpayer_name", ""),
            tax_category=it.get("tax_category", ""),
            sub_type=it.get("sub_type", ""),
            base_amount=it.get("base_amount", 0),
            deductions=it.get("deductions", 0),
            calculated_tax=it.get("calculated_tax", 0),
            status=it.get("status", "รอชำระ"),
            record_id=it.get("id", ""),
            note=it.get("note", "")
        )
        tax_objects.append(record)

    # กรองข้อมูลตามคำค้นหาและหมวดหมู่
    filtered_records = []
    for rec in tax_objects:
        matches_cat = True
        if filter_category and rec.tax_category != filter_category:
            matches_cat = False

        matches_search = True
        if search_keyword:
            in_name = search_keyword in rec.taxpayer_name.lower()
            in_id = search_keyword in rec.record_id.lower()
            in_sub = search_keyword in rec.sub_type.lower()
            matches_search = in_name or in_id or in_sub

        if matches_cat and matches_search:
            filtered_records.append(rec)

    # คำนวณสถิติภาพรวม
    total_tax_all = sum(rec.calculated_tax for rec in tax_objects)
    total_paid = sum(rec.calculated_tax for rec in tax_objects if rec.status == "ชำระแล้ว")
    total_pending = sum(rec.calculated_tax for rec in tax_objects if rec.status == "รอชำระ")
    count_all = len(tax_objects)

    # จำแนกภาษีตาม 4 หมวดหมู่หลัก
    categories_target = [
        "ภาษีเงินได้บุคคลธรรมดา",
        "ภาษีเงินได้นิติบุคคล",
        "ภาษีที่ดินและสิ่งปลูกสร้าง",
        "ภาษีป้าย"
    ]
    breakdown = []
    for cat in categories_target:
        cat_items = [rec for rec in tax_objects if rec.tax_category == cat]
        cat_sum = sum(rec.calculated_tax for rec in cat_items)
        cat_pct = round((cat_sum / total_tax_all * 100.0), 1) if total_tax_all > 0 else 0.0
        breakdown.append({
            "name": cat,
            "count": len(cat_items),
            "total_tax": cat_sum,
            "percentage": cat_pct
        })

    # จัดอันดับผู้เสียภาษีสูงสุด 5 อันดับแรก
    sorted_records = sorted(tax_objects, key=lambda x: x.calculated_tax, reverse=True)
    top_5 = sorted_records[:5]

    return {
        "records": filtered_records,
        "count_all": count_all,
        "total_tax_all": total_tax_all,
        "total_paid": total_paid,
        "total_pending": total_pending,
        "breakdown": breakdown,
        "top_5": top_5,
        "search_keyword": search_keyword,
        "filter_category": filter_category,
        "categories_target": categories_target
    }


def handle(form):
    """ประมวลผลการปรับปรุงสถานะภาษี หรือการคืนค่าข้อมูลเริ่มต้น"""
    if not form:
        return ""

    # การเปลี่ยนสถานะเป็นชำระแล้ว
    toggle_id = form.get("toggle_paid_id")
    if toggle_id:
        items = storage.load()
        found = False
        for it in items:
            if it.get("id") == toggle_id:
                it["status"] = "ชำระแล้ว" if it.get("status") == "รอชำระ" else "รอชำระ"
                found = True
                break
        if found:
            storage.save(items)
            return f"อัปเดตสถานะรายการ {toggle_id} เรียบร้อยแล้ว"

    # การกู้คืนข้อมูลตัวอย่างมาตรฐาน
    if form.get("action") == "reset":
        if storage.reset():
            return "คืนค่าข้อมูลตัวอย่างมาตรฐาน (data.sample.json) สำเร็จแล้ว"

    return "บันทึกการทำงานเรียบร้อย"
