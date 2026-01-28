from odoo import models, fields, tools

class ThongKePhongHop(models.Model):
    _name = 'thong_ke_phong_hop'
    _description = 'Thống kê số lần sử dụng phòng họp & thiết bị'
    _auto = False  # Sử dụng VIEW thay vì bảng thực tế trong database

    phong_hop_id = fields.Many2one('danh_sach_phong_hop', string="Phòng họp", readonly=True)
    so_lan_su_dung = fields.Integer(string="Số lần sử dụng", readonly=True)
    so_thiet_bi_duoc_su_dung = fields.Integer(string="Số thiết bị đã sử dụng", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW thong_ke_phong_hop AS (
                SELECT
                    row_number() OVER () AS id,
                    lsp.phong_hop_id,
                    COUNT(lsp.id) AS so_lan_su_dung,
                    COUNT(DISTINCT tb.id) AS so_thiet_bi_duoc_su_dung
                FROM lich_su_dat_phong lsp
                LEFT JOIN thiet_bi_phong_hop tb
                    ON tb.phong_hop_id = lsp.phong_hop_id
                GROUP BY lsp.phong_hop_id
            )
        """)
