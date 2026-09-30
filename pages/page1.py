"""pages/page1.py — คำนวณภาษีเงินได้บุคคลธรรมดาและนิติบุคคล
ผู้รับผิดชอบ: นางสาวสุพิชญา ปะถะมา (รหัสนักศึกษา 69130840212)
"""
import storage

TITLE = "ภาษีเงินได้บุคคลและนิติบุคคล"


def calculate_personal_tax(income, expenses_allowed, deductions):
    """คำนวณภาษีเงินได้บุคคลธรรมดาตามอัตราก้าวหน้า (Progressive Rate 0% - 35%)"""
    taxable_net = max(0.0, income - expenses_allowed - deductions)

    brackets = [
        (150000, 0.00),
        (150000, 0.05),
        (200000, 0.10),
        (250000, 0.15),
        (250000, 0.20),
        (1000000, 0.25),
        (3000000, 0.30),
        (float("inf"), 0.35)
    ]

    remaining = taxable_net
    total_tax = 0.0

    for bracket_span, rate in brackets:
        if remaining <= 0:
            break
        taxable_in_bracket = min(remaining, bracket_span)
        total_tax += taxable_in_bracket * rate
        remaining -= taxable_in_bracket

    return taxable_net, round(total_tax, 2)


def calculate_corporate_tax(net_profit, corp_type):
    """คำนวณภาษีเงินได้นิติบุคคล (ทั่วไป 20% หรือ อัตราผ่อนปรน SME)"""
    if net_profit <= 0:
        return 0.0

    if corp_type == "sme":
        # SME: กำไร 300,000 ยกเว้น, 300,001-3,000,000 เสีย 15%, ส่วนเกิน 3,000,000 เสีย 20%
        if net_profit <= 300000:
            return 0.0
        elif net_profit <= 3000000:
            return round((net_profit - 300000) * 0.15, 2)
        else:
            tax_tier2 = (3000000 - 300000) * 0.15
            tax_tier3 = (net_profit - 3000000) * 0.20
            return round(tax_tier2 + tax_tier3, 2)
    else:
        # นิติบุคคลทั่วไป: อัตราร้อยละ 20 ของกำไรสุทธิ
        return round(net_profit * 0.20, 2)


def build():
    """ดึงข้อมูลรายการภาษีเงินได้ทั้งหมดเพื่อนำไปแสดงผลบนหน้าเว็บ"""
    items = storage.load()
    income_tax_records = []

    for item in items:
        cat = item.get("tax_category", "")
        if cat in ["ภาษีเงินได้บุคคลธรรมดา", "ภาษีเงินได้นิติบุคคล"]:
            income_tax_records.append(item)

    return {
        "records": income_tax_records,
        "total_count": len(income_tax_records),
    }


def handle(form):
    """ประมวลผลเมื่อผู้ใช้ส่งแบบฟอร์มคำนวณและบันทึกข้อมูลภาษี"""
    if not form:
        return ""

    # กรณีลบรายการ
    delete_id = form.get("delete_id")
    if delete_id:
        items = storage.load()
        updated_items = [it for it in items if it.get("id") != delete_id]
        storage.save(updated_items)
        return f"ลบรายการรหัส {delete_id} เรียบร้อยแล้ว"

    # กรณีบันทึกการคำนวณใหม่
    taxpayer_name = form.get("taxpayer_name", "").strip()
    if not taxpayer_name:
        return "กรุณาระบุชื่อผู้เสียภาษีหรือชื่อนิติบุคคล"

    tax_kind = form.get("tax_kind", "personal")
    items = storage.load()
    new_id = f"TAX-{len(items) + 101}"

    if tax_kind == "personal":
        try:
            income = float(form.get("income", 0) or 0)
        except ValueError:
            income = 0.0

        # หักค่าใช้จ่ายตาม ม.40(1) สูงสุด 50% แต่ไม่เกิน 100,000 บาท
        expenses_allowed = min(income * 0.50, 100000.0)

        # ค่าลดหย่อนส่วนบุคคล 60,000 และประกัน/กองทุน
        personal_deduct = 60000.0
        try:
            insurance = float(form.get("insurance", 0) or 0)
        except ValueError:
            insurance = 0.0

        total_deduct = personal_deduct + min(insurance, 100000.0)
        taxable_net, tax_amount = calculate_personal_tax(income, expenses_allowed, total_deduct)

        effective = round((tax_amount / income) * 100.0, 2) if income > 0 else 0.0

        record = {
            "id": new_id,
            "taxpayer_name": taxpayer_name,
            "tax_category": "ภาษีเงินได้บุคคลธรรมดา",
            "sub_type": "ภ.ง.ด. 91 (เงินเดือนและค่าจ้าง)",
            "base_amount": round(income, 2),
            "deductions": round(expenses_allowed + total_deduct, 2),
            "taxable_base": round(taxable_net, 2),
            "calculated_tax": round(tax_amount, 2),
            "effective_rate": effective,
            "status": form.get("status", "รอชำระ"),
            "note": f"หักค่าใช้จ่าย {expenses_allowed:,.2f} + ลดหย่อน {total_deduct:,.2f}"
        }
    else:
        try:
            net_profit = float(form.get("net_profit", 0) or 0)
        except ValueError:
            net_profit = 0.0

        corp_type = form.get("corp_type", "sme")
        tax_amount = calculate_corporate_tax(net_profit, corp_type)
        sub_type_label = "วิสาหกิจขนาดกลางและขนาดย่อม (SME)" if corp_type == "sme" else "นิติบุคคลทั่วไป"
        effective = round((tax_amount / net_profit) * 100.0, 2) if net_profit > 0 else 0.0

        record = {
            "id": new_id,
            "taxpayer_name": taxpayer_name,
            "tax_category": "ภาษีเงินได้นิติบุคคล",
            "sub_type": sub_type_label,
            "base_amount": round(net_profit, 2),
            "deductions": 0.0,
            "taxable_base": round(net_profit, 2),
            "calculated_tax": round(tax_amount, 2),
            "effective_rate": effective,
            "status": form.get("status", "รอชำระ"),
            "note": f"ประเมินตามเกณฑ์ {sub_type_label}"
        }

    items.append(record)
    storage.save(items)
    return f"ประเมินภาษีสำเร็จ: รหัส {new_id} ({taxpayer_name}) ภาษีที่ต้องชำระ {record['calculated_tax']:,.2f} บาท"
