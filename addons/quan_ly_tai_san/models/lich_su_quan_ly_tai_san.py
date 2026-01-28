from odoo import models, fields

class LichSuQuanLyTaiSan(models.Model):
    _name = 'lich_su_quan_ly_tai_san'
    _description = 'Bảng chứa lịch sử sử dụng tài sản'
    

    # Thông tin mượn/trả
    muon_tra_id = fields.Many2one('muon_tra', string="Mượn/Trả liên quan", )
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


    # Tình trạng tài sản
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