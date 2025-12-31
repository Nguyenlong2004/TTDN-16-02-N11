from odoo import models, fields

class HopDongLaoDong(models.Model):
    _name = 'hop_dong_lao_dong'
    _description = 'Hợp đồng lao động'

    so_hop_dong = fields.Char(string="Số hợp đồng", required=True)
    loai_hop_dong = fields.Selection([
        ('thu_viec', 'Thử việc'),
        ('xac_dinh', 'Xác định thời hạn'),
        ('khong_xac_dinh', 'Không xác định thời hạn'),
    ], string="Loại hợp đồng", required=True, default='thu_viec')

    ngay_bat_dau = fields.Date(string="Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc")
    muc_luong = fields.Float(string="Mức lương")

    nhan_vien_id = fields.Many2one(
        comodel_name='nhan_vien',
        string="Nhân viên",
        ondelete='cascade',
        required=True,
        index=True,
    )
