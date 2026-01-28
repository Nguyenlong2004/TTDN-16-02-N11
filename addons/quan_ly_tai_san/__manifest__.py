# -*- coding: utf-8 -*-
{
    'name': "quan_ly_tai_san",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'nhan_su'],
    
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/tai_san.xml',
        'views/thanh_ly.xml',
        'views/bao_tri.xml',
        'views/muon_tra.xml',
        'views/lich_su_quan_ly_tai_san.xml',
        'views/nha_cung_cap.xml',
        'views/lich_su_su_dung_tai_san.xml',
        'views/danh_muc_loai_tai_san.xml',
        'views/dieu_chuyen_tai_san.xml',
        'views/lich_su_dieu_chuyen_tai_san.xml',
        'views/thong_ke.xml',
        'views/cap_phat_tai_san.xml',
        'views/lich_su_cap_phat_tai_san_view.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
