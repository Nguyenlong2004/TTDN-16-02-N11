from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class DonMuonPhong(models.Model):
    _name = 'don_muon_phong'
    _description = 'Đơn mượn phòng'

    # =====================
    # FIELDS
    # =====================
    ten_don_muon = fields.Char(
        string="Tên đơn mượn",
        required=True
    )

    phong_hop_id = fields.Many2one(
        'danh_sach_phong_hop',
        string='Phòng họp',
        required=True
    )

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên mượn phòng",
        required=True
    )

    thoi_gian_bat_dau = fields.Datetime(
        string="Thời gian bắt đầu",
        required=True
    )

    thoi_gian_ket_thuc = fields.Datetime(
        string="Thời gian kết thúc",
        required=True
    )

    trang_thai = fields.Selection(
        [
            ('pending', 'Chờ xác nhận'),
            ('confirmed', 'Đã xác nhận'),
            ('cancelled', 'Đã hủy'),
        ],
        string="Trạng thái",
        default='pending'
    )

    muc_dich_su_dung = fields.Text(
        string="Mục đích sử dụng"
    )

    lich_su_dat_phong_ids = fields.One2many(
        'lich_su_dat_phong',
        'don_muon_phong_id',
        string="Lịch sử đặt phòng"
    )

    # =====================
    # CONSTRAINT: TIME
    # =====================
    @api.constrains('thoi_gian_bat_dau', 'thoi_gian_ket_thuc')
    def _check_time_constraints(self):
        for record in self:
            if not record.thoi_gian_bat_dau or not record.thoi_gian_ket_thuc:
                continue  # 👈 chưa đủ dữ liệu thì bỏ qua

            if record.thoi_gian_bat_dau >= record.thoi_gian_ket_thuc:
                raise ValidationError(
                    "Thời gian bắt đầu phải trước thời gian kết thúc."
                )

            delta = record.thoi_gian_ket_thuc - record.thoi_gian_bat_dau
            if delta > timedelta(hours=6):
                raise ValidationError(
                    "Thời gian mượn phòng tối đa là 6 giờ."
                )


    # =====================
    # CONSTRAINT: OVERLAP
    # =====================
    @api.constrains('phong_hop_id', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc')
    def _check_room_availability(self):
        for record in self:
            if not record.phong_hop_id:
                continue

            overlapping = self.env['lich_su_dat_phong'].search([
                ('phong_hop_id', '=', record.phong_hop_id.id),
                ('thoi_gian_bat_dau', '<', record.thoi_gian_ket_thuc),
                ('thoi_gian_ket_thuc', '>', record.thoi_gian_bat_dau),
                ('don_muon_phong_id', '!=', record.id),
                ('trang_thai', 'in', ['pending', 'confirmed']),
            ], limit=1)

            if overlapping:
                raise ValidationError(
                    "Phòng họp đã bị đặt trong khoảng thời gian này."
                )

    # =====================
    # ACTIONS
    # =====================
    def action_confirm(self):
        for record in self:
            if record.trang_thai != 'pending':
                continue

            record.trang_thai = 'confirmed'

            # tạo lịch sử đặt phòng
            self.env['lich_su_dat_phong'].create({
                'don_muon_phong_id': record.id,
                'phong_hop_id': record.phong_hop_id.id,
                'nhan_vien_id': record.nhan_vien_id.id, 
                'thoi_gian_bat_dau': record.thoi_gian_bat_dau,
                'thoi_gian_ket_thuc': record.thoi_gian_ket_thuc,
                'trang_thai': 'confirmed',
            })

    def action_cancel(self):
        for record in self:
            record.trang_thai = 'cancelled'

            # cập nhật lịch sử (nếu có)
            record.lich_su_dat_phong_ids.filtered(
                lambda l: l.trang_thai in ['pending', 'confirmed']
            ).write({
                'trang_thai': 'cancelled'
            })

    # =====================
    # NAME GET
    # =====================
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.phong_hop_id.ten_phong} ({record.thoi_gian_bat_dau} → {record.thoi_gian_ket_thuc})"
            result.append((record.id, name))
        return result

    def action_checkin(self):
        self.ensure_one()
        self.env['phong_hop_event'].create({
            'don_muon_phong_id': self.id,
            'nhan_vien_id': self.nhan_vien_id.id,
            'loai_su_kien': 'checkin',
            'thoi_gian': fields.Datetime.now(),
        })
