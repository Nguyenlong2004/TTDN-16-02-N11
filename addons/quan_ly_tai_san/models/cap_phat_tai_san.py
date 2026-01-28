from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CapPhatTaiSan(models.Model):
    _name = 'qlts.cap_phat_tai_san'
    _description = 'Cấp phát tài sản'
    _order = 'ngay_cap_phat desc'

    ma_phieu = fields.Char(
        string="Mã cấp phát",
        required=True,
        copy=False,
        default="New"
    )

    tai_san_id = fields.Many2one(
        'tai_san',
        string="Tài sản",
        required=True
    )

    so_luong = fields.Integer(
        string="Số lượng cấp phát",
        default=1
    )

    vi_tri_cap_phat_id = fields.Many2one(
        'qlts.vi_tri_tai_san',
        string="Vị trí nhận",
        required=True
    )

    nhan_vien_nhan_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên nhận"
    )

    phong_ban_nhan_id = fields.Many2one(
        'phong_ban',
        string="Phòng ban nhận"
    )

    ngay_cap_phat = fields.Date(
        string="Ngày cấp phát",
        default=fields.Date.today
    )

    nguoi_cap_phat_id = fields.Many2one(
        'res.users',
        string="Người cấp phát",
        default=lambda self: self.env.user
    )
    
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('da_cap_phat', 'Đã cấp phát'),
        ('thu_hoi', 'Đã thu hồi'),
    ], default='draft')

    ghi_chu = fields.Text()    

    @api.onchange('tai_san_id')
    def _onchange_tai_san_id(self):
        if self.tai_san_id:
            self.vi_tri_cap_phat_id = self.tai_san_id.vi_tri_hien_tai_id

    @api.onchange('phong_ban_nhan_id')
    def _onchange_phong_ban_nhan_id(self):
            if self.phong_ban_nhan_id:
                self.nhan_vien_nhan_id = False
                return {
                    'domain': {
                        'nhan_vien_nhan_id': [
                            ('phong_ban_id', '=', self.phong_ban_nhan_id.id)
                        ]
                    }
                }
    def action_da_cap_phat(self):
        for record in self:
            if record.trang_thai == 'da_cap_phat':
                continue

            if record.so_luong <= 0:
                raise ValidationError("Số lượng cấp phát phải lớn hơn 0!")

            tai_san = record.tai_san_id

            if record.so_luong > tai_san.so_luong:
                raise ValidationError(
                    f"Số lượng tồn không đủ! Hiện còn {tai_san.so_luong}"
                )

            # 🔥 TRỪ SỐ LƯỢNG TÀI SẢN
            tai_san.write({
                'so_luong': tai_san.so_luong - record.so_luong
            })
            # 🔥 TẠO LỊCH SỬ CẤP PHÁT
            self.env['qlts.lich_su_cap_phat'].create({
            'cap_phat_id': record.id,
            'tai_san_id': record.tai_san_id.id,
            'so_luong': record.so_luong,
            'nhan_vien_id': record.nhan_vien_nhan_id.id,
            'phong_ban_id': record.phong_ban_nhan_id.id,
            'vi_tri_id': record.vi_tri_cap_phat_id.id,
            'loai': 'cap_phat',
            'ngay_thuc_hien': record.ngay_cap_phat,
            'nguoi_thuc_hien_id': self.env.user.id,
            'ghi_chu': record.ghi_chu,
            })
            # 🔄 CẬP NHẬT TRẠNG THÁI
            record.trang_thai = 'da_cap_phat'
    