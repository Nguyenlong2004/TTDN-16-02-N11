from odoo import models, fields, api


class MuonTra(models.Model):
    _name = 'muon_tra'
    _description = 'Quản lý nhân viên/phòng ban mượn tài sản'
    _rec_name = "ma_muon"

    ma_muon = fields.Char("Mã mượn/trả", required=True, copy=False, readonly=True, default="New")
    nhan_vien_id = fields.Many2one('nhan_vien', string="Mã nhân viên", required=True)
    ho_va_ten = fields.Char(related='nhan_vien_id.ho_va_ten', string="Tên nhân viên", readonly=True)
    phong_ban_id = fields.Many2one(related='nhan_vien_id.phong_ban_id', string="Phòng ban", readonly=True)
    chuc_vu_id = fields.Many2one(related='nhan_vien_id.chuc_vu_id', string="Chức vụ", readonly=True)
    tai_san_id = fields.Many2one('tai_san', string="Mã tài sản", required=True)
    ten_tai_san = fields.Char(related='tai_san_id.ten_tai_san', string="Tên tài sản", readonly=True)
    thoi_gian_muon = fields.Date("Thời gian mượn", required=True, default=fields.Date.today)
    thoi_gian_tra_du_kien = fields.Date("Thời gian trả dự kiến")
    thoi_gian_tra_thuc_te = fields.Date("Thời gian trả thực tế")
    
    trang_thai = fields.Selection([
        ('dang_muon', 'Đang mượn'),
        ('da_tra', 'Đã trả'),
        ('qua_han', 'Quá hạn')
    ], string="Trạng thái", compute="_kiem_tra_trang_thai", store=True)

    ghi_chu = fields.Text("Ghi chú")


    @api.depends('thoi_gian_tra_du_kien', 'thoi_gian_tra_thuc_te')
    def _kiem_tra_trang_thai(self):
        for record in self:
            if record.thoi_gian_tra_thuc_te:
                record.trang_thai = 'da_tra'
            elif record.thoi_gian_tra_du_kien and record.thoi_gian_tra_du_kien < fields.Date.today():
                record.trang_thai = 'qua_han'
            else:
                record.trang_thai = 'dang_muon'

    @api.model
    def create(self, vals):
        """Tạo mã mượn/trả tự động & tạo lịch sử sử dụng tài sản"""
        if vals.get('ma_muon', 'New') == 'New':
            last_record = self.search([], order="id desc", limit=1)
            last_number = int(last_record.ma_muon[2:]) if last_record and last_record.ma_muon.startswith("MT") else 0
            vals['ma_muon'] = f"MT{last_number + 1:05d}"

        record = super(MuonTra, self).create(vals)

        # Tạo bản ghi trong lịch sử sử dụng tài sản
        self.env['lich_su_su_dung_tai_san'].create({
            'muon_tra_id': record.id,
            'tai_san_id': record.tai_san_id.id,
            'ten_tai_san': record.ten_tai_san,
            'nhan_vien_id': record.nhan_vien_id.id,
            'ho_va_ten': record.ho_va_ten,
            'phong_ban_id': record.phong_ban_id.id,
            'chuc_vu_id': record.chuc_vu_id.id,
            'ngay_muon': record.thoi_gian_muon,
            'trang_thai': record.trang_thai,
            'tinh_trang_truoc': 'tot',  # Giá trị mặc định
        })

        return record

    def write(self, vals):
        """Cập nhật lịch sử sử dụng tài sản khi có thay đổi"""
        res = super(MuonTra, self).write(vals)

        for record in self:
            history = self.env['lich_su_su_dung_tai_san'].search([('muon_tra_id', '=', record.id)], limit=1)
            if history:
                update_vals = {}
                if 'trang_thai' in vals:
                    update_vals['trang_thai'] = vals['trang_thai']
                if 'thoi_gian_tra_thuc_te' in vals:
                    update_vals['ngay_tra'] = vals['thoi_gian_tra_thuc_te']
                if update_vals:
                    history.write(update_vals)

        return res
    
    def xuat_don_muon(self):
        """Gọi hàm xuất hợp đồng mượn tài sản"""
        return self.env['don_muon'].export_muon_tra_docx(self.id)


