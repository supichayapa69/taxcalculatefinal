"""pages/page2.py — คำนวณภาษีที่ดินและสิ่งปลูกสร้าง และภาษีป้าย
ผู้รับผิดชอบ: นางสาวนันท์ภัส พิมพ์ภักดิ์ (รหัสนักศึกษา 69130840076)
"""
import math
import storage

TITLE = "ภาษีที่ดินและภาษีป้าย"


def calculate_land_building_tax(land_type, appraisal_value):
    """คำนวณภาษีที่ดินและสิ่งปลูกสร้างตาม พ.ร.บ. ภาษีที่ดินและสิ่งปลูกสร้าง พ.ศ. 2562"""
    deduction = 0.0
    tax = 0.0

    if land_type == "agri":
        # เกษตรกรรม (บุคคลธรรมดา): ยกเว้น 50 ล้านบาทแรก
        deduction = min(appraisal_value, 50000000.0)
        taxable = max(0.0, appraisal_value - deduction)
        tax = taxable * 0.0001  # อัตรา 0.01%
    elif land_type == "home_main":
        # ที่อยู่อาศัยหลังหลัก (เป็นเจ้าของที่ดินและสิ่งปลูกสร้าง): ยกเว้น 50 ล้านบาทแรก
        deduction = min(appraisal_value, 50000000.0)
        taxable = max(0.0, appraisal_value - deduction)
        tax = taxable * 0.0002  # อัตรา 0.02%
    elif land_type == "home_sub":
        # ที่อยู่อาศัยหลังอื่น (บ้านหลังที่ 2 / ปล่อยเช่า): ไม่มียกเว้น
        deduction = 0.0
        taxable = appraisal_value
        tax = taxable * 0.0002  # อัตราเริ่มต้น 0.02%
    elif land_type == "commercial":
        # อื่นๆ / พาณิชยกรรม / อุตสาหกรรม
        deduction = 0.0
        taxable = appraisal_value
        if taxable <= 50000000:
            tax = taxable * 0.003  # ร้อยละ 0.30%
        else:
            tax = (50000000 * 0.003) + ((taxable - 50000000) * 0.004)
    else:  # vacant - รกร้างว่างเปล่า
        deduction = 0.0
        taxable = appraisal_value
        tax = taxable * 0.003  # ร้อยละ 0.30%

    return deduction, taxable, round(tax, 2)


def calculate_signboard_tax(width_cm, height_cm, sign_type, is_moving):
    """คำนวณภาษีป้ายตามกฎกระทรวงกำหนดอัตราภาษีป้าย พ.ศ. 2563 (ขั้นต่ำ 200 บาท)"""
    area_sq_cm = max(1.0, width_cm * height_cm)
    units_500 = math.ceil(area_sq_cm / 500.0)

    # อัตราภาษีต่อ 500 ตารางเซนติเมตร
    if sign_type == "1":
        # ประเภท 1: อักษรไทยล้วน
        rate_per_unit = 10 if is_moving else 5
    elif sign_type == "2":
        # ประเภท 2: อักษรไทยปนอักษรต่างประเทศ หรือภาพ/เครื่องหมาย
        rate_per_unit = 52 if is_moving else 26
    else:
        # ประเภท 3: ไม่มีอักษรไทย หรืออักษรไทยอยู่ต่ำกว่าอักษรต่างประเทศ
        rate_per_unit = 52 if is_moving else 50

    raw_tax = units_500 * rate_per_unit
    # กฎหมายกำหนดว่า หากคำนวณแล้วต่ำกว่า 200 บาท ให้เสียขั้นต่ำ 200 บาท
    final_tax = max(200.0, float(raw_tax))

    return area_sq_cm, units_500, final_tax


def build():
    """ดึงข้อมูลรายการภาษีที่ดินและภาษีป้ายทั้งหมดเพื่อนำไปแสดงผล"""
    items = storage.load()
    local_tax_records = []

    for item in items:
        cat = item.get("tax_category", "")
        if cat in ["ภาษีที่ดินและสิ่งปลูกสร้าง", "ภาษีป้าย"]:
            local_tax_records.append(item)

    return {
        "records": local_tax_records,
        "total_count": len(local_tax_records),
    }


def handle(form):
    """ประมวลผลการคำนวณและบันทึกภาษีท้องถิ่น"""
    if not form:
        return ""

    # กรณีลบรายการ
    delete_id = form.get("delete_id")
    if delete_id:
        items = storage.load()
        items = [it for it in items if it.get("id") != delete_id]
        storage.save(items)
        return f"ลบรายการรหัส {delete_id} เรียบร้อยแล้ว"

    taxpayer_name = form.get("taxpayer_name", "").strip()
    if not taxpayer_name:
        return "กรุณาระบุชื่อผู้เสียภาษีหรือชื่อสถานประกอบการ"

    tax_kind = form.get("tax_kind", "land")
    items = storage.load()
    new_id = f"TAX-{len(items) + 101}"

    if tax_kind == "land":
        try:
            appraisal = float(form.get("appraisal_value", 0) or 0)
        except ValueError:
            appraisal = 0.0

        land_type = form.get("land_type", "home_main")
        type_labels = {
            "agri": "เกษตรกรรม (บุคคลธรรมดา)",
            "home_main": "ที่อยู่อาศัย (บ้านหลังหลัก)",
            "home_sub": "ที่อยู่อาศัย (บ้านหลังอื่น/ปล่อยเช่า)",
            "commercial": "การใช้ประโยชน์อื่น/พาณิชยกรรม",
            "vacant": "ที่ดินรกร้างว่างเปล่าไม่ได้ทำประโยชน์"
        }
        sub_type_label = type_labels.get(land_type, "ที่อยู่อาศัย")

        deduction, taxable, tax_amount = calculate_land_building_tax(land_type, appraisal)
        effective = round((tax_amount / appraisal) * 100.0, 4) if appraisal > 0 else 0.0

        record = {
            "id": new_id,
            "taxpayer_name": taxpayer_name,
            "tax_category": "ภาษีที่ดินและสิ่งปลูกสร้าง",
            "sub_type": sub_type_label,
            "base_amount": round(appraisal, 2),
            "deductions": round(deduction, 2),
            "taxable_base": round(taxable, 2),
            "calculated_tax": round(tax_amount, 2),
            "effective_rate": effective,
            "status": form.get("status", "รอชำระ"),
            "note": f"คำนวณตามเกณฑ์ {sub_type_label} (พ.ร.บ.ภาษีที่ดินฯ)"
        }
    else:  # signboard
        try:
            width = float(form.get("width", 0) or 0)
            height = float(form.get("height", 0) or 0)
        except ValueError:
            width, height = 0.0, 0.0

        sign_type = form.get("sign_type", "1")
        is_moving = form.get("is_moving") == "yes"

        type_names = {
            "1": "ป้ายอักษรไทยล้วน",
            "2": "ป้ายอักษรไทยปนอักษรต่างประเทศ",
            "3": "ป้ายไม่มีอักษรไทย/อักษรไทยอยู่ต่ำกว่าต่างประเทศ"
        }
        sub_type_label = type_names.get(sign_type, "ป้ายอักษรไทยล้วน")
        if is_moving:
            sub_type_label += " (มีข้อความเคลื่อนไหว)"

        area, units, tax_amount = calculate_signboard_tax(width, height, sign_type, is_moving)
        effective = round((tax_amount / area) * 100.0, 2) if area > 0 else 0.0

        record = {
            "id": new_id,
            "taxpayer_name": taxpayer_name,
            "tax_category": "ภาษีป้าย",
            "sub_type": sub_type_label,
            "base_amount": round(area, 2),
            "deductions": 0.0,
            "taxable_base": round(area, 2),
            "calculated_tax": round(tax_amount, 2),
            "effective_rate": effective,
            "status": form.get("status", "รอชำระ"),
            "note": f"ขนาด {area:,.0f} ตร.ซม. ({units} หน่วย) กฎกระทรวงปี 2563"
        }

    items.append(record)
    storage.save(items)
    return f"ประเมินภาษีท้องถิ่นสำเร็จ: รหัส {new_id} ({taxpayer_name}) ภาษีที่ต้องชำระ {record['calculated_tax']:,.2f} บาท"
