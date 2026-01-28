from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SuCoPhongHop(models.Model):
    _name = 'su_co_phong_hop'
    _description = 'Sự cố phòng họp'
    _order = 'thoi_gian_bao desc'
    _rec_name = 'ten_su_co'

    ten_su_co = fields.Char(
        string="Tên sự cố",
        required=True
    )

    phong_hop_id = fields.Many2one(
        'danh_sach_phong_hop',
        string="Phòng họp",
        required=True,
        ondelete='cascade'
    )

    don_muon_id = fields.Many2one(
        'don_muon_phong',
        string="Đơn mượn phòng"
    )

    nguoi_bao_id = fields.Many2one(
        'nhan_vien',
        string="Người báo sự cố",
        required=True
    )

    thoi_gian_bao = fields.Datetime(
        string="Thời gian báo",
        default=fields.Datetime.now,
        required=True
    )

    mo_ta = fields.Text(
        string="Mô tả chi tiết"
    )

    muc_do = fields.Selection(
        [
            ('nhe', 'Nhẹ'),
            ('trung_binh', 'Trung bình'),
            ('nghiem_trong', 'Nghiêm trọng')
        ],
        string="Mức độ",
        default='nhe',
        required=True
    )

    trang_thai = fields.Selection(
        [
            ('moi', 'Mới báo'),
            ('dang_xu_ly', 'Đang xử lý'),
            ('da_xu_ly', 'Đã xử lý')
        ],
        string="Trạng thái",
        default='moi',
        tracking=True
    )

    nguoi_xu_ly_id = fields.Many2one(
        'nhan_vien',
        string="Người xử lý"
    )

    thoi_gian_xu_ly = fields.Datetime(
        string="Thời gian xử lý"
    )

    ghi_chu_xu_ly = fields.Text(
        string="Ghi chú xử lý"
    )

    # -------------------------
    # CONSTRAINT NGHIỆP VỤ
    # -------------------------
    @api.constrains('thoi_gian_xu_ly', 'thoi_gian_bao')
    def _check_thoi_gian(self):
        for rec in self:
            if rec.thoi_gian_xu_ly and rec.thoi_gian_xu_ly < rec.thoi_gian_bao:
                raise ValidationError(
                    "Thời gian xử lý không được nhỏ hơn thời gian báo sự cố!"
                )
    def action_goi_y_phong_trong(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Gợi ý phòng họp trống',
            'res_model': 'goi_y_phong_hop_trong',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_id': self.id,
                'default_su_co_id': self.id,
            }
    }
