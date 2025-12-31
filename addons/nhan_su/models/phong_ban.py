from odoo import models, fields

class phongban(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'
    _oder = 'ma_phong_ban'
    _rec_name = 'ten_phong_ban'

    ma_phong_ban = fields.Char("Mã phòng ban", required=True)
    ten_phong_ban = fields.Char("Tên phòng ban", required=True)
    mo_ta = fields.Text("Mô tả")
    nhan_vien_ids = fields.Many2many(comodel_name='nhan_vien', string="Nhan vien")