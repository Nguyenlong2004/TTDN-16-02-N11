from odoo import models, fields, api

class ThietBiPhongHop(models.Model):
    _name = "thiet_bi_phong_hop"
    _description = "Thiết bị phòng họp"

    ten_thiet_bi = fields.Char(string="Tên thiết bị", required=True)
    serial_number = fields.Char(string="Số serial",unique=True)
    loai_thiet_bi = fields.Selection([
        ('may_chieu', 'Máy chiếu'),
        ('loa', 'Loa'),
        ('micro', 'Micro'),
        ('khac', 'Khác'),
    ], string="Loại thiết bị", required=True)
    image = fields.Binary(string="Hình ảnh thiết bị")
    
    trang_thai = fields.Selection([
        ('tot', 'Tốt'),
        ('can_bao_tri', 'Cần bảo trì'),
        ('hong', 'Hỏng'),
    ], string="Trạng thái", default="tot")

    phong_hop_id = fields.Many2one("danh_sach_phong_hop", string="Phòng họp", store = True)

    @api.onchange('trang_thai')
    def _onchange_trang_thai(self):
        """ Cập nhật trạng thái thiết bị khi có thay đổi """
        if self.trang_thai == 'can_bao_tri':
            self.phong_hop_id.trang_thai = 'Cần bảo trì'
            
    def name_get(self):
        """ Đảm bảo tên thiết bị hiển thị chính xác """
        result = []
        for record in self:
            result.append((record.id, record.ten_thiet_bi))  # Trả về tên thiết bị
        return result
