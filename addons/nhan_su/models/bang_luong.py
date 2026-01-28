from odoo import models, fields, api


class BangLuong(models.Model):
    _name = 'bang_luong'
    _description = 'Bảng lương'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    thang = fields.Integer("Tháng", default=lambda self: fields.Date.today().month)
    nam = fields.Integer("Năm", default=lambda self: fields.Date.today().year)
    ngay_bang_luong = fields.Date("Ngày bảng lương", default=fields.Date.today)
    so_ngay_lam_viec = fields.Float("Số ngày làm việc chuẩn", default=26)
    luong_co_ban = fields.Float(related='nhan_vien_id.luong_co_ban', string="Lương cơ bản", readonly=True)
    so_cong = fields.Float("Số công", compute="_compute_so_cong")
    luong_theo_cong = fields.Float("Lương theo công", compute="_compute_luong_theo_cong", store=True)
    thuong = fields.Float("Thưởng")
    phat = fields.Float("Phạt")
    luong_nhan = fields.Float("Lương nhận", compute="_compute_luong_nhan", store=True)
    cham_cong_ids = fields.One2many('nhan_su.cham_cong', 'nhan_vien_id', string="Chi tiết chấm công")

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_so_cong(self):
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                start_date = f'{record.nam}-{record.thang:02d}-01'
                if record.thang == 12:
                    end_date = f'{record.nam+1}-01-01'
                else:
                    end_date = f'{record.nam}-{record.thang+1:02d}-01'
                cham_cong_records = self.env['nhan_su.cham_cong'].search([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id),
                    ('ngay_cham_cong', '>=', start_date),
                    ('ngay_cham_cong', '<', end_date)
                ])
                total_gio_lam = sum(r.so_gio_lam for r in cham_cong_records)
                # 8 giờ = 1 công
                record.so_cong = total_gio_lam / 8
            else:
                record.so_cong = 0

    @api.depends('so_cong', 'luong_co_ban', 'so_ngay_lam_viec')
    def _compute_luong_theo_cong(self):
        for record in self:
            if record.so_ngay_lam_viec and record.so_ngay_lam_viec != 0 and record.luong_co_ban:
                record.luong_theo_cong = record.so_cong * (record.luong_co_ban / record.so_ngay_lam_viec)
            else:
                record.luong_theo_cong = 0

    @api.depends('luong_theo_cong', 'thuong', 'phat')
    def _compute_luong_nhan(self):
        for record in self:
            record.luong_nhan = record.luong_theo_cong + (record.thuong or 0) - (record.phat or 0)

    _sql_constraints = [
        ('unique_nhan_vien_thang_nam', 'unique(nhan_vien_id, thang, nam)', 'Mỗi nhân viên chỉ có một bảng lương cho mỗi tháng!')
    ]