from odoo import models, fields, api

class DanhMucLoaiTaiSan(models.Model):
    _name = 'danh_muc_loai_tai_san'
    _description = 'Danh mục loại tài sản'
    _rec_name = "ten_loai_tai_san"

    ma_loai_tai_san = fields.Char("Mã loại tài sản", required=True, copy=False, readonly=True, default="New")
    ten_loai_tai_san = fields.Char("Tên loại tài sản", required=True)
    nhom_tai_san_id = fields.Char("Nhóm tài sản", required=True)
    
    phuong_thuc_khau_hao = fields.Selection([
        ('duong_thang', 'Khấu hao đường thẳng'),
        ('giam_dan', 'Khấu hao theo số dư giảm dần'),
        ('san_pham', 'Khấu hao theo sản lượng'),
    ], string="Phương thức khấu hao", required=True, default='duong_thang')

    thoi_gian_khau_hao = fields.Integer("Thời gian khấu hao (năm)", required=True)
    ty_le_khau_hao = fields.Float("Tỷ lệ khấu hao hàng năm (%)", compute="_tinh_ty_le_khau_hao", store=True)
    
    tai_san_ids = fields.One2many('tai_san', 'danh_muc_loai_tai_san_id', string="Danh sách tài sản")
    
    mo_ta = fields.Text("Mô tả chi tiết")

    @api.depends('thoi_gian_khau_hao')
    def _tinh_ty_le_khau_hao(self):
        for record in self:
            record.ty_le_khau_hao = 100.0 / record.thoi_gian_khau_hao if record.thoi_gian_khau_hao > 0 else 0.0

    @api.model
    def create(self, vals):
        if vals.get('ma_loai_tai_san', 'New') == 'New':
            last_record = self.search([], order="id desc", limit=1)
            last_number = int(last_record.ma_loai_tai_san[3:]) if last_record and last_record.ma_loai_tai_san.startswith("LTS") else 0
            vals['ma_loai_tai_san'] = f"LTS{last_number + 1:04d}"

        return super(DanhMucLoaiTaiSan, self).create(vals)