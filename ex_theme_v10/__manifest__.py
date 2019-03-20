# -*- coding: utf-8 -*-
{
    'name': "ex_theme_v10",

    'summary': """
       皮肤
       """,

    'description': """
        皮肤
    """,

    'author': "zzw",
    'website': "",

    'category': 'Theme',
    'version': '0.1',

    'depends': ['web'],

    'data': [
        'views/webclient_templates.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'sequence': 1,
    'application': True,
}
