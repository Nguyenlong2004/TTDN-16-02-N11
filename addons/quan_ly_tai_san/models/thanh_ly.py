from odoo import models, fields, api

class ThanhLy(models.Model):
    _name = 'thanh_ly'
    _description = 'Bảng chứa thông tin thanh lý tài sản'
    _rec_name = "ten_tai_san"  # Tên hiển thị đại diện

    ma_thanh_ly = fields.Char("Mã thanh lý", required=True, copy=False, readonly=True, default="New")
    tai_san_id = fields.Many2one('tai_san', string="Mã tài sản", required=True)
    ten_tai_san = fields.Char(related='tai_san_id.ten_tai_san', string="Tên tài sản", readonly=True)
    ngay_thanh_ly = fields.Date("Ngày thanh lý")
    gia_tri_thanh_ly = fields.Char("Giá trị thanh lý")
    nha_cung_cap_id = fields.Many2one('nha_cung_cap', string="Người thanh lý", required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Mã phê duyệt", required=True)
    nguoi_phe_duyet = fields.Char(related='nhan_vien_id.ho_va_ten', string="Người phê duyệt", readonly=True)
    chuc_vu_id = fields.Many2one(related='nhan_vien_id.chuc_vu_id', string="Chức vụ", readonly=True)
    ghi_chu = fields.Text("Ghi chú")
    thong_ke_id = fields.Many2one('thong_ke', string="Thống kê liên quan")    
    trang_thai_tai_san = fields.Selection(related='tai_san_id.trang_thai', string="Trạng thái tài sản", store=True,readonly=True)

#    người thanh ý và ng phê duyêt tách riêngriêng
    @api.model
    def create(self, vals):
        if vals.get('ma_thanh_ly', 'New') == 'New':
            last_record = self.search([], order="id desc", limit=1)
            
            if last_record and last_record.ma_thanh_ly and last_record.ma_thanh_ly.startswith("TL"):
                try:
                    last_number = int(last_record.ma_thanh_ly[2:])
                except ValueError:
                    last_number = 0
            else:
                last_number = 0
            
            new_number = last_number + 1
            vals['ma_thanh_ly'] = f"TL{new_number:05d}"
        
        return super(ThanhLy, self).create(vals)
    def action_xac_nhan_thanh_ly(self):
        for record in self:
            tai_san = record.tai_san_id
            if tai_san.trang_thai == 'da_thanh_ly':
                raise ValidationError("Tài sản này đã được thanh lý trước đó!")
            # 🔥 ĐÁNH DẤU TÀI SẢN ĐÃ THANH LÝ
            tai_san.write({
                'trang_thai': 'da_thanh_ly',
                'so_luong': 0,
            })