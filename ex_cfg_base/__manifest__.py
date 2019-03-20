# -*- coding: utf-8 -*-
{
    'name': "ex_cfg_base",

    'summary': """
        平台配置数据库(主数据平台) """,

    'description':
    '''
        1、服务管理
        2、消息通道管理
        3、用户管理
    ''',

    'author': "zzw",
    'website': "",

    'category': 'school',
    'version': '0.1',

    'depends': ['mail'],

    'data': [
        'views/ex_class.xml',
        'views/ex_key.xml',
        'views/ex_teacher.xml',
        'views/ex_parent.xml',
        'views/ex_student.xml',
        'views/ex_app_tpl.xml',
        'views/ex_cfg_school.xml',
        'views/ex_cfg_sms.xml',
        'views/ex_cfg_wechat.xml',
        'views/class_teacher_rel.xml',
        'views/menu.xml',
    ],
    'application':True,
}