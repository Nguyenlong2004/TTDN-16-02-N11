from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_va_ten'
    _order = 'ten asc, tuoi desc'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)

    ho_ten_dem = fields.Char("Họ tên đệm", required=True)
    ten = fields.Char("Tên", required=True)
    ho_va_ten = fields.Char("Họ và tên", compute="_compute_ho_va_ten", store=True)

    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")

    lich_su_cong_tac_ids = fields.One2many(
        "lich_su_cong_tac",
        inverse_name="nhan_vien_id",
        string="Danh sách lịch sử công tác"
    )

    ma_cham_cong = fields.One2many(
        'nhan_su.cham_cong',
        'nhan_vien_id',
        string="Chấm công"
    )

    hop_dong_lao_dong_ids = fields.One2many(
        'hop_dong_lao_dong',
        'nhan_vien_id',
        string="Hợp đồng lao động"
    )

    bang_luong_ids = fields.One2many(
        'bang_luong',
        'nhan_vien_id',
        string="Bảng lương"
    )
    chuc_vu_id = fields.Many2one(
    'chuc_vu',
    string="Chức vụ"
    )

    tuoi = fields.Integer("Tuổi", compute="_compute_tuoi", store=True)
    anh = fields.Binary("Ảnh")
    luong_co_ban = fields.Float("Lương cơ bản")

    danh_sach_chung_chi_bang_cap_ids = fields.One2many(
        "danh_sach_chung_chi_bang_cap",
        inverse_name="nhan_vien_id",
        string="Danh sách chứng chỉ bằng cấp"
    )

    so_nguoi_bang_tuoi = fields.Integer(
        "Số người bằng tuổi",
        compute="_compute_so_nguoi_bang_tuoi",
        store=True
    )
    
    phong_ban_id = fields.Many2one(
        'phong_ban',
        string="Phòng ban"
    )

    so_a = fields.Integer(string="Số a")
    so_b = fields.Integer(string="Số b")
    tong_ab = fields.Integer(string="Tổng a+b", compute="_compute_tong_ab", store=True)

    @api.depends('so_a', 'so_b')
    def _compute_tong_ab(self):
        for record in self:
            record.tong_ab = (record.so_a or 0) + (record.so_b or 0)

    # ✅ FIX CHUẨN Ở ĐÂY
    @api.depends("tuoi")
    def _compute_so_nguoi_bang_tuoi(self):
        for record in self:
            if record.tuoi and record.id:
                records = self.env['nhan_vien'].search([
                    ('tuoi', '=', record.tuoi),
                    ('id', '!=', record.id),
                ])
                record.so_nguoi_bang_tuoi = len(records)
            else:
                record.so_nguoi_bang_tuoi = 0

    _sql_constraints = [
        ('ma_dinh_danh_unique', 'unique(ma_dinh_danh)', 'Mã định danh phải là duy nhất')
    ]

    @api.depends("ho_ten_dem", "ten")
    def _compute_ho_va_ten(self):
        for record in self:
            record.ho_va_ten = (record.ho_ten_dem or '').strip() + ' ' + (record.ten or '').strip()

    @api.onchange("ten", "ho_ten_dem")
    def _default_ma_dinh_danh(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                chu_cai_dau = ''.join(
                    [tu[0][0] for tu in record.ho_ten_dem.lower().split() if tu]
                )
                record.ma_dinh_danh = record.ten.lower() + chu_cai_dau

    @api.depends("ngay_sinh")
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                year_now = date.today().year
                record.tuoi = year_now - record.ngay_sinh.year
            else:
                record.tuoi = 0

    @api.constrains('tuoi')
    def _check_tuoi(self):
        for record in self:
            if record.tuoi and record.tuoi < 18:
                raise ValidationError("Tuổi không được bé hơn 18")

