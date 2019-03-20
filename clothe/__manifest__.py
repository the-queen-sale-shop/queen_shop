# -*- coding: utf-8 -*-
{
    'name': "clothe",

    'summary': """
        clothe """,

    'description':
        '''
    
        ''',

    'author': "ss",
    'website': "",

    'category': 'clothe',
    'version': '0.1',

    # 'depends': ['mail','ex_theme_v10','ex_web_login','web_export_view_good','report_docx','ir_sequence_autoreset'],
    'depends': ['mail', 'ex_theme_v10', 'ex_web_login', 'web_export_view_good', 'report_docx'],

    'data': [
        # 权限
        'security/groups.xml',
        'security/ir.model.access.csv',
        # 基础数据
        'views/base/order.xml',
        'views/base/order_item.xml',
        'views/base/people.xml',
        'views/base/stock.xml',
        'views/base/report.xml',

        # 菜单
        'views/menu.xml',

    ],
    'application': True,
}
