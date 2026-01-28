from datetime import timedelta
from odoo import models, fields, api, exceptions


class LichSuDatPhong(models.Model):
    _name = "lich_su_dat_phong"
    _description = "Lịch sử đặt phòng"

    phong_hop_id = fields.Many2one(
        "danh_sach_phong_hop", string="Phòng họp", required=True
    )
    nhan_vien_id = fields.Many2one(
        "nhan_vien", string="Người đặt", required=True
    )
    thoi_gian_bat_dau = fields.Datetime(
        string="Thời gian bắt đầu", required=True
    )
    thoi_gian_ket_thuc = fields.Datetime(
        string="Thời gian kết thúc", required=True
    )
    don_muon_phong_id = fields.Many2one(
        'don_muon_phong', string="Đơn mượn phòng"
    )
    vi_tri_id = fields.Many2one(
        'vi_tri_phong_hop',
        string="Vị trí phòng",
        related='phong_hop_id.vi_tri_id',
        store=True,
        readonly=True
    )

    trang_thai = fields.Selection(
        [
            ('pending', 'Chờ'),
            ('confirmed', 'Đã xác nhận'),
            ('done', 'Hoàn thành'),
            ('cancelled', 'Hủy'),
        ],
        string="Trạng thái",
        default='confirmed'
    )

    # =====================
    # CREATE HISTORY
    # =====================
    @api.model
    def create_history(self, don_muon_phong):
        existing_history = self.search([
            ('don_muon_phong_id', '=', don_muon_phong.id),
            ('trang_thai', 'in', ['pending', 'confirmed'])
        ], limit=1)

        if not existing_history:
            self.create({
                'don_muon_phong_id': don_muon_phong.id,
                'nhan_vien_id': don_muon_phong.nhan_vien_id.id,
                'phong_hop_id': don_muon_phong.phong_hop_id.id,
                'thoi_gian_bat_dau': don_muon_phong.thoi_gian_bat_dau,
                'thoi_gian_ket_thuc': don_muon_phong.thoi_gian_ket_thuc,
                'trang_thai': 'confirmed',
            })

    # =====================
    # CONSTRAINT: TIME
    # =====================
    @api.constrains('thoi_gian_bat_dau', 'thoi_gian_ket_thuc')
    def _check_time_constraints(self):
        for record in self:
            if not record.thoi_gian_bat_dau or not record.thoi_gian_ket_thuc:
                continue

            if record.thoi_gian_bat_dau >= record.thoi_gian_ket_thuc:
                raise exceptions.ValidationError(
                    "Thời gian bắt đầu phải trước thời gian kết thúc."
                )

            delta = record.thoi_gian_ket_thuc - record.thoi_gian_bat_dau
            if delta > timedelta(hours=6):
                raise exceptions.ValidationError(
                    "Thời gian mượn phòng tối đa là 6 giờ."
                )

    # =====================
    # CRON: AUTO DONE
    # =====================
    @api.model
    def cron_update_lich_su_done(self):
        now = fields.Datetime.now()
        records = self.search([
            ('trang_thai', '=', 'confirmed'),
            ('thoi_gian_ket_thuc', '<', now)
        ])
        records.write({'trang_thai': 'done'})

    # =====================
    # NAME GET
    # =====================
    def name_get(self):
        result = []
        for record in self:
            name = (
                f"{record.phong_hop_id.ten_phong} "
                f"({record.thoi_gian_bat_dau} → {record.thoi_gian_ket_thuc})"
            )
            result.append((record.id, name))
        return result
