"""models.py — คลาสแบบจำลองข้อมูลภาษีตามกฎหมายไทย
ผู้รับผิดชอบ: นางสาวประภาสินีย์ อิ่นคำ (รหัสนักศึกษา 69130840342)
"""


class TaxRecord:
    """แบบจำลองข้อมูลรายการภาษีและงบประมาณตามระเบียบราชการไทย"""

    def __init__(self, taxpayer_name, tax_category, sub_type, base_amount,
                 deductions=0, calculated_tax=0, status="รอชำระ", record_id=None, note=""):
        self.record_id = record_id or "TAX-000"
        self.taxpayer_name = str(taxpayer_name).strip()
        self.tax_category = str(tax_category).strip()
        self.sub_type = str(sub_type).strip()
        self.base_amount = float(base_amount) if base_amount else 0.0
        self.deductions = float(deductions) if deductions else 0.0
        self.taxable_base = max(0.0, self.base_amount - self.deductions)
        self.calculated_tax = float(calculated_tax) if calculated_tax else 0.0
        self.status = str(status).strip() or "รอชำระ"
        self.note = str(note).strip()

    def describe(self):
        """สรุปข้อมูลรายการภาษีในรูปแบบทางการ"""
        formatted_base = f"{self.base_amount:,.2f}"
        formatted_tax = f"{self.calculated_tax:,.2f}"
        return (f"[{self.record_id}] ผู้เสียภาษี: {self.taxpayer_name} | "
                f"ประเภท: {self.tax_category} ({self.sub_type}) | "
                f"ฐานประเมิน: {formatted_base} บาท | ภาษีที่ต้องชำระ: {formatted_tax} บาท "
                f"({self.status})")

    def get_effective_rate(self):
        """คำนวณอัตราภาษีที่แท้จริง (Effective Tax Rate ร้อยละ)"""
        if self.base_amount <= 0:
            return 0.0
        rate = (self.calculated_tax / self.base_amount) * 100.0
        return round(rate, 2)

    def to_dict(self):
        """แปลงออบเจกต์เป็น Dictionary สำหรับบันทึกลง data.json"""
        return {
            "id": self.record_id,
            "taxpayer_name": self.taxpayer_name,
            "tax_category": self.tax_category,
            "sub_type": self.sub_type,
            "base_amount": round(self.base_amount, 2),
            "deductions": round(self.deductions, 2),
            "taxable_base": round(self.taxable_base, 2),
            "calculated_tax": round(self.calculated_tax, 2),
            "effective_rate": self.get_effective_rate(),
            "status": self.status,
            "note": self.note
        }
