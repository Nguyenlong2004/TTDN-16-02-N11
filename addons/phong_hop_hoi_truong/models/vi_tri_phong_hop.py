from odoo import models, fields

from odoo import models, fields

class ViTriPhongHop(models.Model):
    _name = "vi_tri_phong_hop"
    _description = "Vị trí phòng họp"

    name = fields.Char(string="Tên vị trí", required=True)
    toa_nha = fields.Char(string="Tòa nhà")
    tang = fields.Char(string="Tầng")
    ghi_chu = fields.Text(string="Ghi chú")

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.toa_nha or record.tang:
                name = f"{name} - {record.toa_nha or ''} {record.tang or ''}".strip()
            result.append((record.id, name))
        return result
