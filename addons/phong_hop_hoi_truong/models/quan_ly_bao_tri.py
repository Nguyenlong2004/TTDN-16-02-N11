from odoo import models, fields, api


class QuanLyBaoTri(models.Model):
    _name = "quan_ly_bao_tri"
    _description = "Quản lý bảo trì"


    nhan_vien_id = fields.Many2one(
        "nhan_vien",
        string="Nhân viên bảo trì",
        required=True
    )

    ngay_bao_tri = fields.Date(
        string="Ngày bảo trì",
        required=True
    )
    phong_hop_id = fields.Many2one(
        'danh_sach_phong_hop',
        string='Phòng họp',
        required=True
    )
    
    ghi_chu = fields.Text(string="Ghi chú")

    trang_thai = fields.Selection(
        [
            ('dang_bao_tri', 'Đang bảo trì'),
            ('hoan_thanh', 'Hoàn thành'),
        ],
        string="Trạng thái",
        default="dang_bao_tri"
    )
