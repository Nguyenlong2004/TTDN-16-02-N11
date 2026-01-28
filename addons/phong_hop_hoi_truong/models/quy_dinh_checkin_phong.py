from odoo import models, fields


class QuyDinhCheckinPhong(models.Model):
    _name = 'quy_dinh_checkin_phong'
    _description = 'Quy định check-in phòng họp'

    bat_buoc_checkin = fields.Boolean(
        string="Bắt buộc check-in bằng QR",
        default=True
    )

    thoi_gian_cho_checkin = fields.Integer(
        string="Thời gian cho phép check-in (phút)",
        help="Số phút sau giờ bắt đầu được phép check-in"
    )

    tu_dong_huy_neu_khong_checkin = fields.Boolean(
        string="Tự động hủy nếu không check-in",
        default=False
    )

    ghi_chu = fields.Text(string="Ghi chú")
