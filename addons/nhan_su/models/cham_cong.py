from odoo import models, fields, api


class ChamCong(models.Model):
    _name = 'nhan_su.cham_cong'
    _description = 'Chấm công'

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên",
        required=True
    )

    ngay_cham_cong = fields.Date(
        "Ngày chấm công",
        required=True,
        default=fields.Date.today
    )

    # Float nhưng sẽ nhập theo dạng HH:MM
    gio_vao = fields.Float(
        "Giờ vào",
        help="Nhập theo dạng HH:MM (VD: 07:30)"
    )

    gio_ra = fields.Float(
        "Giờ ra",
        help="Nhập theo dạng HH:MM (VD: 17:00)"
    )

    gio_nghi = fields.Float(
        "Giờ nghỉ",
        default=1,
        help="Số giờ nghỉ (VD: 1 = nghỉ 1 tiếng)"
    )

    so_gio_lam = fields.Float(
        "Số giờ làm",
        compute="_compute_so_gio_lam",
        store=True
    )

    trang_thai = fields.Selection([
        ('du_cong', 'Đủ công'),
        ('thieu_cong', 'Thiếu công'),
        ('di_muon', 'Đi muộn'),
        ('ve_som', 'Về sớm'),
        ('nghi', 'Nghỉ')
    ], string="Trạng thái", default='du_cong')

    @api.depends('gio_vao', 'gio_ra', 'gio_nghi')
    def _compute_so_gio_lam(self):
        for record in self:
            if record.gio_vao and record.gio_ra:
                tong_gio = record.gio_ra - record.gio_vao
                record.so_gio_lam = max(tong_gio - (record.gio_nghi or 0), 0)
            else:
                record.so_gio_lam = 0
