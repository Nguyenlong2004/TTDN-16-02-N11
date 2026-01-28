from odoo import models, fields, api

class LichSuDieuChuyenTaiSan(models.Model):
    _name = 'lich_su_dieu_chuyen_tai_san'
    _description = 'Lịch sử điều chuyển tài sản'
    
    dieu_chuyen_tai_san_id = fields.Many2one('dieu_chuyen_tai_san', string="Phiếu điều chuyển", required=True, ondelete='cascade')
    
    # Thông tin điều chuyển (TỰ ĐỘNG LẤY TỪ dieu_chuyen_tai_san)
    ma_dieu_chuyen = fields.Char(related='dieu_chuyen_tai_san_id.ma_dieu_chuyen', string="Mã điều chuyển", readonly=True, store=True)
    tai_san_id = fields.Many2one(related='dieu_chuyen_tai_san_id.tai_san_id', string="Mã tài sản", readonly=True, store=True)
    ten_tai_san = fields.Char(related='dieu_chuyen_tai_san_id.ten_tai_san', string="Tên tài sản", readonly=True, store=True)
    tu_dia_diem = fields.Many2one(related='dieu_chuyen_tai_san_id.tu_dia_diem', string="Địa điểm hiện tại", readonly=True, store=True)
    den_dia_diem = fields.Many2one(related='dieu_chuyen_tai_san_id.den_dia_diem', string="Địa điểm chuyển đi", readonly=True, store=True)
    ngay_dieu_chuyen = fields.Date(related='dieu_chuyen_tai_san_id.ngay_dieu_chuyen', string="Ngày điều chuyển", readonly=True, store=True)
    nguoi_phe_duyet = fields.Char(related='dieu_chuyen_tai_san_id.nguoi_phe_duyet', string="Người phê duyệt", readonly=True, store=True)
    trang_thai = fields.Selection(related='dieu_chuyen_tai_san_id.trang_thai', string="Trạng thái", readonly=True, store=True)
    ghi_chu = fields.Text(related='dieu_chuyen_tai_san_id.ghi_chu', string="Ghi chú", readonly=True, store=True)

    @api.model
    def create_from_dieu_chuyen_tai_san(self, dieu_chuyen_tai_san):
        """Tạo bản ghi lịch sử từ phiếu điều chuyển"""
        return self.create({
            'dieu_chuyen_tai_san_id': dieu_chuyen_tai_san.id,
        })

    @api.model
    def auto_create_lich_su(self):
        """Tự động tạo lịch sử cho các phiếu Điều Chuyển chưa có lịch sử"""
        dieu_chuyen_records = self.env['dieu_chuyen_tai_san'].search([
            ('id', 'not in', self.search([]).mapped('dieu_chuyen_tai_san_id').ids)
        ])
        for dieu_chuyen_tai_san in dieu_chuyen_records:
            self.create_from_dieu_chuyen_tai_san(dieu_chuyen_tai_san)
    