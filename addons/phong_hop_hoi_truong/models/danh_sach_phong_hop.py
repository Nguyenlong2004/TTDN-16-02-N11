from odoo import models, fields, api


class DanhSachPhongHop(models.Model):
    _name = "danh_sach_phong_hop"
    _description = "Danh sách phòng họp"

    ten_phong = fields.Char(string="Tên phòng", required=True)
    suc_chua = fields.Integer(string="Sức chứa")

    vi_tri_id = fields.Many2one(
        'vi_tri_phong_hop',
        string="Vị trí",
        required=True
    )
    
    trang_thai = fields.Selection(
        [
            ('available', 'Trống'),
            ('using', 'Đang sử dụng'),
            ('maintenance', 'Bảo trì'),
        ],
        string="Trạng thái",
        compute="_compute_trang_thai",
        store=True
    )

    lich_su_dat_phong_ids = fields.One2many(
        "lich_su_dat_phong",
        "phong_hop_id",
        string="Lịch sử đặt phòng"
    )

    thoi_gian_ket_thuc_hien_tai = fields.Datetime(
        string="Sử dụng đến",
        compute="_compute_thoi_gian_ket_thuc_hien_tai"
    )

    hinh_anh_phong_hop = fields.Binary(
    string="Hình ảnh phòng họp"
    )

    # ===== COMPUTE =====
    @api.depends(
    'lich_su_dat_phong_ids.trang_thai',
    'lich_su_dat_phong_ids.thoi_gian_bat_dau',
    'lich_su_dat_phong_ids.thoi_gian_ket_thuc',
    )
    def _compute_trang_thai(self):
        now = fields.Datetime.now()

        for record in self:
            record.trang_thai = 'available'

            # Có lịch đang sử dụng
            dang_dung = record.lich_su_dat_phong_ids.filtered(
                lambda l: l.trang_thai == 'confirmed'
                and l.thoi_gian_bat_dau <= now <= l.thoi_gian_ket_thuc
            )
            if dang_dung:
                record.trang_thai = 'using'


    @api.depends(
        'lich_su_dat_phong_ids.trang_thai',
        'lich_su_dat_phong_ids.thoi_gian_bat_dau',
        'lich_su_dat_phong_ids.thoi_gian_ket_thuc',
    )
    def _compute_thoi_gian_ket_thuc_hien_tai(self):
        now = fields.Datetime.now()
        for record in self:
            record.thoi_gian_ket_thuc_hien_tai = False

            lich = record.lich_su_dat_phong_ids.filtered(
                lambda l: l.trang_thai == 'confirmed'
                and l.thoi_gian_bat_dau <= now <= l.thoi_gian_ket_thuc
            )
            if lich:
                record.thoi_gian_ket_thuc_hien_tai = lich[0].thoi_gian_ket_thuc

    def name_get(self):
        return [(r.id, r.ten_phong) for r in self]
