from odoo import models, fields, api

class LichSuTaiSan(models.Model):
    _name = 'lich_su_su_dung_tai_san'
    _description = 'Bảng chứa lịch sử sử dụng tài sản'
    
    # Liên kết với mượn/trả
    muon_tra_id = fields.Many2one('muon_tra', string="Mượn/Trả liên quan", required=True, ondelete='cascade')

    # Thông tin mượn/trả (TỰ ĐỘNG LẤY TỪ muon_tra)
    ngay_muon = fields.Date(related='muon_tra_id.thoi_gian_muon', string="Thời gian nhận tài sản", readonly=True, store=True)
    ngay_tra = fields.Date(related='muon_tra_id.thoi_gian_tra_thuc_te', string="Thời gian trả tài sản", readonly=True, store=True)
    trang_thai = fields.Selection(related='muon_tra_id.trang_thai', string="Trạng thái", readonly=True, store=True)

    # Thông tin tài sản
    tai_san_id = fields.Many2one(related='muon_tra_id.tai_san_id', string="Mã tài sản", readonly=True, store=True)
    ten_tai_san = fields.Char(related='muon_tra_id.ten_tai_san', string="Tên tài sản", readonly=True, store=True)

    # Thông tin nhân viên
    nhan_vien_id = fields.Many2one(related='muon_tra_id.nhan_vien_id', string="Mã nhân viên", readonly=True, store=True)
    ho_va_ten = fields.Char(related='muon_tra_id.ho_va_ten', string="Tên nhân viên", readonly=True, store=True)
    phong_ban_id = fields.Many2one(related='muon_tra_id.phong_ban_id', string="Phòng ban", readonly=True, store=True)
    chuc_vu_id = fields.Many2one(related='muon_tra_id.chuc_vu_id', string="Chức vụ", readonly=True, store=True)

    # Người kiểm tra tài sản
    nguoi_kiem_tra = fields.Many2one("res.users", string="Người phê duyệt")

    # Tình trạng tài sản trước và sau khi sử dụng
    tinh_trang_tai_san = [
        ('tot', 'Tốt'),
        ('binh_thuong', 'Bình thường'),
        ('hu_hong_nhe', 'Hư hỏng nhẹ'),
        ('hu_hong_nang', 'Hư hỏng nặng'),
        ('mat_tai_san', 'Mất tài sản')
    ]

    tinh_trang_truoc = fields.Selection(
        selection=tinh_trang_tai_san, 
        string="Tình trạng trước khi sử dụng", 
        default='tot', 
        required=True, 
    )

    tinh_trang_sau = fields.Selection(
        selection=tinh_trang_tai_san, 
        string="Tình trạng sau khi sử dụng", 
        default='tot', 
    )

    @api.model
    def create(self, vals):
        """Tự động tạo lịch sử khi có phiếu mượn mới."""
        record = super(LichSuTaiSan, self).create(vals)
        return record

    @api.model
    def create_from_muon_tra(self, muon_tra):
        """Tạo bản ghi lịch sử từ phiếu Mượn/Trả"""
        return self.create({
            'muon_tra_id': muon_tra.id,
            'nguoi_kiem_tra': muon_tra.create_uid.id,
        })

    @api.model
    def auto_create_lich_su(self):
        """Tự động tạo lịch sử cho các phiếu Mượn/Trả chưa có lịch sử"""
        muon_tra_records = self.env['muon_tra'].search([('id', 'not in', self.search([]).mapped('muon_tra_id').ids)])
        for muon_tra in muon_tra_records:
            self.create_from_muon_tra(muon_tra)
