from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DieuChuyenTaiSan(models.Model):
    _name = 'dieu_chuyen_tai_san'
    _description = 'Quản lý điều chuyển tài sản'
    _rec_name = "ma_dieu_chuyen"

    ma_dieu_chuyen = fields.Char("Mã điều chuyển", required=True, copy=False, readonly=True, default="New")
    tai_san_id = fields.Many2one('tai_san', string="Mã tài sản", required=True)
    ten_tai_san = fields.Char(related='tai_san_id.ten_tai_san', string="Tên tài sản", readonly=True)
    tu_dia_diem = fields.Many2one('qlts.vi_tri_tai_san', string="Địa điểm hiện tại", required=True)
    den_dia_diem = fields.Many2one('qlts.vi_tri_tai_san', string="Địa điểm chuyển đi", required=True)
    ngay_dieu_chuyen = fields.Date("Thời gian điều chuyển", required=True, default=fields.Date.today)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Họ và tên người phê duyệt", required=True)
    nguoi_phe_duyet = fields.Char(related='nhan_vien_id.ho_va_ten', string="Người phê duyệt", readonly=True)
    thong_ke_id = fields.Many2one('thong_ke', string="Thống kê liên quan")    

    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('hoan_thanh', 'Hoàn thành'),
    ], string="Trạng thái", default='cho_duyet')
    
    ghi_chu = fields.Text("Ghi chú")

    @api.model
    def create(self, vals):
        """Tạo mã điều chuyển tự động và ghi lịch sử điều chuyển."""
        if vals.get('ma_dieu_chuyen', 'New') == 'New':
            last_record = self.search([], order="id desc", limit=1)
            last_number = 0  
            
            if last_record and last_record.ma_dieu_chuyen and last_record.ma_dieu_chuyen.startswith("DC"):
                try:
                    last_number = int(last_record.ma_dieu_chuyen[2:])
                except ValueError:
                    last_number = 0  

            vals['ma_dieu_chuyen'] = f"DC{last_number + 1:04d}"

        dieu_chuyen_tai_san = super(DieuChuyenTaiSan, self).create(vals)

        # Tạo lịch sử điều chuyển tài sản
        self.env['lich_su_dieu_chuyen_tai_san'].create({
            'dieu_chuyen_tai_san_id': dieu_chuyen_tai_san.id,
        })

        return dieu_chuyen_tai_san

    @api.onchange('tai_san_id')
    def _onchange_tai_san_id(self):
        if self.tai_san_id:
            self.tu_dia_diem = self.tai_san_id.vi_tri_hien_tai_id
    def action_da_duyet(self):
        for record in self:
            if not record.den_dia_diem:
                raise ValidationError("Bạn chưa chọn địa điểm chuyển đến!")

            record.tai_san_id.write({
                'vi_tri_hien_tai_id': record.den_dia_diem.id
            })
            record.trang_thai = 'da_duyet'
    def action_hoan_thanh(self):
        for record in self:
            if not record.den_dia_diem:
                raise ValidationError("Chưa có địa điểm chuyển đến!")

            # CẬP NHẬT VỊ TRÍ TÀI SẢN
            record.tai_san_id.write({
                'vi_tri_hien_tai_id': record.den_dia_diem.id
            })

            record.trang_thai = 'hoan_thanh'

