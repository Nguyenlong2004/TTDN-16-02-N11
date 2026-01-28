from odoo import models, fields

class LichSuCapPhatTaiSan(models.Model):
    _name = 'qlts.lich_su_cap_phat'
    _description = 'Lịch sử cấp phát tài sản'
    _order = 'ngay_thuc_hien desc'

    cap_phat_id = fields.Many2one(
        'qlts.cap_phat_tai_san',
        string="Phiếu cấp phát",
        ondelete='cascade'
    )

    tai_san_id = fields.Many2one(
        'tai_san',
        string="Tài sản",
        required=True
    )

    so_luong = fields.Integer(
        string="Số lượng"
    )

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên nhận"
    )

    phong_ban_id = fields.Many2one(
        'phong_ban',
        string="Phòng ban"
    )

    vi_tri_id = fields.Many2one(
        'qlts.vi_tri_tai_san',
        string="Vị trí"
    )

    loai = fields.Selection([
        ('cap_phat', 'Cấp phát'),
        ('thu_hoi', 'Thu hồi')
    ], string="Loại", required=True)

    ngay_thuc_hien = fields.Date(
        string="Ngày thực hiện",
        default=fields.Date.today
    )
    
    nguoi_thuc_hien_id = fields.Many2one(
        'res.users',
        string="Người thực hiện",
        default=lambda self: self.env.user
    )

    ghi_chu = fields.Text()
