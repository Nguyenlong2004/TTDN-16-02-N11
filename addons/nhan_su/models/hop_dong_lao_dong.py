from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
    @api.onchange('loai_hop_dong')
    def _onchange_loai_hop_dong(self):
        if self.loai_hop_dong == 'khong_xac_dinh':
            self.ngay_ket_thuc = False
    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc', 'loai_hop_dong')
    def _check_ngay_ket_thuc(self):
        for record in self:
            if record.loai_hop_dong != 'khong_xac_dinh':
                if not record.ngay_ket_thuc:
                    raise ValidationError("Ngày kết thúc hợp đồng phải được điền cho loại hợp đồng này.")
                if record.ngay_ket_thuc <= record.ngay_bat_dau:
                    raise ValidationError("Ngày kết thúc phải sau ngày bắt đầu.")        
    @api.constrains('loai_hop_dong', 'ngay_ket_thuc')
    def _check_ngay_ket_thuc(self):
        for rec in self:
            if rec.loai_hop_dong == 'khong_xac_dinh' and rec.ngay_ket_thuc:
                raise ValidationError(
                    "Hợp đồng không xác định thời hạn không được có ngày kết thúc!"
                )