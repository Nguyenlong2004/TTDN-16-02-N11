from odoo import models, fields, api

class NhaCungCap(models.Model):
    _name = 'nha_cung_cap'
    _description = 'Bảng chứa thông tin nhà cung cấp'
    _rec_name = "ten_nha_cung_cap"  # Tên hiển thị đại diện

    ma_nha_cung_cap = fields.Char("Mã nhà cung cấp", required=True)
    ten_nha_cung_cap = fields.Char("Tên nhà cung cấp", required=True)
    so_dien_thoai = fields.Char("Số điện thoại")
    email = fields.Char("Email")
    website = fields.Char("Website")
    dia_chi = fields.Text("Địa chỉ")
    ghi_chu = fields.Text("Ghi chú")
