from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PhongHopEvent(models.Model):
    _name = 'phong_hop_event'
    _description = 'Sự kiện phòng họp'
    _order = 'thoi_gian desc'

    don_muon_phong_id = fields.Many2one(
        'don_muon_phong',
        string='Đơn mượn phòng',
        required=True,
        ondelete='cascade'
    )

    phong_hop_id = fields.Many2one(
        related='don_muon_phong_id.phong_hop_id',
        store=True,
        readonly=True
    )

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        required=True
    )

    loai_su_kien = fields.Selection([
        ('checkin', 'Check-in'),
        ('checkout', 'Check-out'),
        ('qr_scan', 'Quét QR'),
        ('manual', 'Thao tác thủ công'),
        ('admin', 'Can thiệp admin'),
    ], required=True)

    thoi_gian = fields.Datetime(
        default=fields.Datetime.now,
        required=True
    )

    qr_token = fields.Char()
    hop_le = fields.Boolean(default=True)
    ghi_chu = fields.Char()
    dia_diem = fields.Char()


    @api.constrains('don_muon_phong_id', 'loai_su_kien')
    def _check_duplicate_checkin(self):
        for rec in self:
            if rec.loai_su_kien != 'checkin':
                continue

            existed = self.search([
                ('id', '!=', rec.id),
                ('don_muon_phong_id', '=', rec.don_muon_phong_id.id),
                ('loai_su_kien', '=', 'checkin'),
            ], limit=1)

            if existed:
                raise ValidationError(
                    "Đơn mượn phòng này đã được check-in rồi."
                )
