from odoo import models, fields, api

class TaiSan(models.Model):
    _name = 'tai_san'
    _description = 'Bảng quản lý tài sản'
    _rec_name = "ma_tai_san"

    # Thông tin cơ bản
    ma_tai_san = fields.Char("Mã tài sản", required=True, copy=False, readonly=True, default="New")
    ten_tai_san = fields.Char("Tên tài sản", required=True)
    
    # Liên kết danh mục loại tài sản
    danh_muc_loai_tai_san_id = fields.Many2one('danh_muc_loai_tai_san', string="Loại tài sản", required=True)
    vi_tri_hien_tai_id = fields.Many2one('qlts.vi_tri_tai_san', string='Vị trí hiện tại')
    nha_cung_cap = fields.Char("Nhà cung cấp")
    cap_phat_ids = fields.One2many('qlts.cap_phat_tai_san','tai_san_id',string="Lịch sử cấp phát")
    
    # Thông tin tài chính
    so_luong = fields.Integer("Số lượng", default=1)
    gia_tri_tai_san = fields.Float("Giá trị tài sản", required=True)
    tong_gia_tri = fields.Float("Tổng giá trị", compute="_compute_tong_gia_tri", store=True)
    het_han_bao_hanh = fields.Date("Hết hạn bảo hành")
    ngay_mua = fields.Date("Thời gian mua")
    thoi_gian_su_dung = fields.Integer("Thời gian sử dụng (năm)", default=5)
    gia_tri_con_lai = fields.Float("Giá trị còn lại (VNĐ)", compute="_compute_gia_tri_con_lai", store=True)
    khau_hao_moi_nam = fields.Integer(related='danh_muc_loai_tai_san_id.thoi_gian_khau_hao',string = "Khấu hao mỗi năm (VNĐ)", compute="_compute_khau_hao", store=True)
    ty_le_khau_hao = fields.Float(related='danh_muc_loai_tai_san_id.ty_le_khau_hao',string = "Tỷ lệ khấu hao hàng năm (%)" ,store=True)
    thong_ke_id = fields.Many2one('thong_ke', string="Thống kê liên quan")    
    # Trạng thái tài sản
    hien_trang_su_dung = fields.Selection([
        ("dang_su_dung", "Đang sử dụng"),
        ("khong_su_dung", "Không sử dụng"),
    ], string="Hiện trạng sử dụng", default="dang_su_dung")

    trang_thai = fields.Selection([
        ("dang_su_dung", "Đang sử dụng"),
        ("hong", "Hỏng"),
        ("mat", "Mất"),
        ("bao_tri", "Bảo trì"),
        ("sua_chua", "Sửa chữa"),
        ("cho_cap_phat", "Đang chờ cấp phát"),
        ("da_thanh_ly", "Đã thanh lý"),
    ], string="Trạng thái", default="dang_su_dung")
    
    # Thống kê số lần sử dụng
    so_lan_muon = fields.Integer("Số lần mượn", compute="_compute_so_lan_muon", store=True)
    so_lan_su_dung = fields.Integer("Số lần sử dụng", compute="_compute_so_lan_su_dung", store=True)
    so_lan_bao_tri = fields.Integer("Số lần bảo trì", compute="_compute_so_lan_bao_tri", store=True)
    so_lan_thanh_ly = fields.Integer("Số lần thanh lý", compute="_compute_so_lan_thanh_ly", store=True)
    so_lan_dieu_chuyen = fields.Integer("Số lần điều chuyển", compute="_compute_so_lan_dieu_chuyen", store=True)

    # Quan hệ One2many
    muon_tra_ids = fields.One2many('muon_tra', 'tai_san_id', string="Lịch sử mượn trả")
    lich_su_su_dung_tai_san_ids = fields.One2many('lich_su_su_dung_tai_san', 'tai_san_id', string="Lịch sử sử dụng")
    lich_su_bao_tri_tai_san_ids = fields.One2many('bao_tri', 'tai_san_id', string="Lịch sử bảo trì")
    lich_su_thanh_ly_tai_san_ids = fields.One2many('thanh_ly', 'tai_san_id', string="Lịch sử thanh lý")
    lich_su_dieu_chuyen_tai_san_ids = fields.One2many('lich_su_dieu_chuyen_tai_san', 'tai_san_id', string="Lịch sử điều chuyển tài sản")

    # === COMPUTE FUNCTIONS ===
    @api.depends('so_luong', 'gia_tri_tai_san')
    def _compute_tong_gia_tri(self):
        for record in self:
            record.tong_gia_tri = record.so_luong * record.gia_tri_tai_san

    @api.depends('ngay_mua', 'thoi_gian_su_dung', 'gia_tri_tai_san')
    def _compute_gia_tri_con_lai(self):
        for record in self:
            if record.ngay_mua:
                years_used = (fields.Date.today() - record.ngay_mua).days // 365
                record.gia_tri_con_lai = max(record.gia_tri_tai_san - (record.khau_hao_moi_nam * years_used), 0)
            else:
                record.gia_tri_con_lai = record.gia_tri_tai_san

    @api.depends('thoi_gian_su_dung', 'gia_tri_tai_san')
    def _compute_khau_hao(self):
        for record in self:
            record.khau_hao_moi_nam = record.gia_tri_tai_san / record.thoi_gian_su_dung if record.thoi_gian_su_dung else 0

    @api.depends('muon_tra_ids')
    def _compute_so_lan_muon(self):
        for record in self:
            record.so_lan_muon = len(record.muon_tra_ids)

    @api.depends('lich_su_su_dung_tai_san_ids')
    def _compute_so_lan_su_dung(self):
        for record in self:
            record.so_lan_su_dung = len(record.lich_su_su_dung_tai_san_ids)

    @api.depends('lich_su_bao_tri_tai_san_ids')
    def _compute_so_lan_bao_tri(self):
        for record in self:
            record.so_lan_bao_tri = len(record.lich_su_bao_tri_tai_san_ids)

    @api.depends('lich_su_thanh_ly_tai_san_ids')
    def _compute_so_lan_thanh_ly(self):
        for record in self:
            record.so_lan_thanh_ly = len(record.lich_su_thanh_ly_tai_san_ids)

    @api.depends('lich_su_dieu_chuyen_tai_san_ids')
    def _compute_so_lan_dieu_chuyen(self):
        for record in self:
            record.so_lan_dieu_chuyen = len(record.lich_su_dieu_chuyen_tai_san_ids)
            
    # === AUTO-GENERATE MA TAI SAN ===
    @api.model
    def create(self, vals):
        if vals.get('ma_tai_san', 'New') == 'New':
            last_record = self.search([], order="id desc", limit=1)
            last_number = int(last_record.ma_tai_san[3:]) if last_record and last_record.ma_tai_san.startswith("MTS") else 0
            vals['ma_tai_san'] = f"MTS{last_number + 1:05d}"
        return super(TaiSan, self).create(vals)
    
    