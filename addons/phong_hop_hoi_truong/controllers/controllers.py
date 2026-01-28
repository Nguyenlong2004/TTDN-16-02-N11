# -*- coding: utf-8 -*-
# from odoo import http


# class PhongHopHoiTruong(http.Controller):
#     @http.route('/phong_hop_hoi_truong/phong_hop_hoi_truong', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/phong_hop_hoi_truong/phong_hop_hoi_truong/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('phong_hop_hoi_truong.listing', {
#             'root': '/phong_hop_hoi_truong/phong_hop_hoi_truong',
#             'objects': http.request.env['phong_hop_hoi_truong.phong_hop_hoi_truong'].search([]),
#         })

#     @http.route('/phong_hop_hoi_truong/phong_hop_hoi_truong/objects/<model("phong_hop_hoi_truong.phong_hop_hoi_truong"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('phong_hop_hoi_truong.object', {
#             'object': obj
#         })
