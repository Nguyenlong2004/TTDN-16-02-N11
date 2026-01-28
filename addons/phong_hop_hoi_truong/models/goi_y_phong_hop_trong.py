from odoo import models, fields, api


class GoiYPhongHopTrong(models.TransientModel):
    _name = 'goi_y_phong_hop_trong'
    _description = 'Gợi ý phòng họp trống'

    su_co_id = fields.Many2one(
        'su_co_phong_hop',
        string="Sự cố phòng họp",
        required=True
    )

    phong_goi_y_ids = fields.Many2many(
        'danh_sach_phong_hop',
        string="Phòng họp trống"
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        su_co = self.env['su_co_phong_hop'].browse(
            self.env.context.get('active_id')
        )

        if not su_co or not su_co.don_muon_id:
            return res

        don = su_co.don_muon_id

        # 1️⃣ Tìm các đơn mượn bị trùng thời gian
        don_trung_lich = self.env['don_muon_phong'].search([
            ('thoi_gian_bat_dau', '<', don.thoi_gian_ket_thuc),
            ('thoi_gian_ket_thuc', '>', don.thoi_gian_bat_dau),
        ])

        # 2️⃣ Lấy các phòng đang bận
        phong_dang_ban = don_trung_lich.mapped('phong_hop_id').ids

        # 3️⃣ Tìm phòng trống
        phong_trong = self.env['danh_sach_phong_hop'].search([
            ('id', 'not in', phong_dang_ban),
            ('id', '!=', su_co.phong_hop_id.id),
            ('trang_thai', '=', 'available'),
        ])

        res['phong_goi_y_ids'] = [(6, 0, phong_trong.ids)]
        return res
