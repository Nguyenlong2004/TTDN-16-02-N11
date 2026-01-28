from odoo import models, fields, api

class BaoTri(models.Model):
    _name = 'bao_tri'
    _description = 'Bảng chứa thông tin bảo trì, bảo dưỡng tài sản'
    _rec_name = "ma_bao_tri"  # Tên hiển thị đại diện

    ma_bao_tri = fields.Char("Mã bảo trì", required=True, copy=False, readonly=True, default="New")
    tai_san_id = fields.Many2one('tai_san', string="Mã tài sản", required=True)
    ten_tai_san = fields.Char(related='tai_san_id.ten_tai_san', string="Tên tài sản", readonly=True)
    ngay_bao_tri = fields.Date("Thời gian bảo trì")  # Sửa mô tả
    noi_dung_bao_tri = fields.Text("Nội dung bảo trì")
    chi_phi_bao_tri = fields.Char("Chi phí bảo trì")
    nha_cung_cap_id = fields.Many2one('nha_cung_cap', string="Người bảo trì", required=True)
    ghi_chu = fields.Text("Ghi chú")
    thong_ke_id = fields.Many2one('thong_ke', string="Thống kê liên quan")    

    tinh_trang = fields.Selection(
        [
            ("da_xong", "Đã xong"),
            ("dang_cho_duyet", "Đang chờ duyệt"),
            ("dang_bao_tri", "Đang bảo trì"),
        ],
        string="Tình trạng",
        default="da_xong"
    )
    @api.model
    def create(self, vals):
        if vals.get('ma_bao_tri', 'New') == 'New':
            last_record = self.search([], order="id desc", limit=1)
            
            if last_record and last_record.ma_bao_tri and last_record.ma_bao_tri.startswith("BC"):
                try:
                    last_number = int(last_record.ma_bao_tri[2:])
                except ValueError:
                    last_number = 0
            else:
                last_number = 0
            
            new_number = last_number + 1
            vals['ma_bao_tri'] = f"BC{new_number:05d}"
        
        return super(BaoTri, self).create(vals)