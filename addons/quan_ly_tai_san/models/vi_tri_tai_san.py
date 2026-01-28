from odoo import models, fields

class ViTriTaiSan(models.Model):
    _name = 'qlts.vi_tri_tai_san'
    _description = 'Vị trí tài sản'
    _rec_name = 'ten_vi_tri' 

    ma_vi_tri = fields.Char(required=True)
    ten_vi_tri = fields.Char(required=True)
    loai_vi_tri = fields.Selection([
        ('phong', 'Phòng'),
        ('kho', 'Kho'),
        ('nguoi', 'Cá nhân'),
        ('khac', 'Khác'),
    ], default='phong')

    ghi_chu = fields.Text()
