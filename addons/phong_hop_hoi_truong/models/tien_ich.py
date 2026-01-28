from odoo import models, fields, api


class TienIch(models.Model):
    _name = 'tien_ich'
    _description = 'Tiện Ích Phòng Họp'

    name = fields.Char(string='Tên Tiện Ích', required=True)
    mo_ta = fields.Text(string='Mô Tả')
    phong_hop_id = fields.Many2one('phong_hop', string='Phòng Họp', required=True)
    is_available = fields.Boolean(string='Có Sẵn', default=True)

    @api.model
    def create(self, vals):
        record = super(TienIch, self).create(vals)
        # Logic bổ sung sau khi tạo tiện ích
        return record

    def toggle_availability(self):
        for record in self:
            record.is_available = not record.is_available