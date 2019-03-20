# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
import os
import json,urllib2
_logger = logging.getLogger(__name__)

class ex_cfg_school(models.Model):
    _name = 'ex.cfg.school'
    _rec_name = 'fullname'
    _description = u'学校'

    fullname = fields.Char("学校中文名称")
    servicename = fields.Char("服务名称")

    odoohost = fields.Char("odoohost")
    odooport = fields.Char("odooport")
    odoo_path = fields.Char("odoo_path")
    odooadminpwd = fields.Char("odooadminpwd")
    dbip = fields.Char("数据库ip")
    dbport = fields.Char("数据库端口")
    dbusername = fields.Char("数据库账号")
    dbpassword = fields.Char("数据库密码")

    webhost = fields.Char("域名")


    # 一所学校的应用只能挂在一个终端下面（企业号、服务号）
    we_ref = fields.Many2one('ex.cfg.wechat', "微信通道")
    sms_ref = fields.Many2one('ex.cfg.sms', "SMS通道")
    we_cfg_ref = fields.Many2one('ex.cfg.wechat.cfg', "微信通道配置")

    address = fields.Char(u"地址")
    web = fields.Char(u"网址")
    isactive = fields.Boolean("账套有效", default=True)

    app_ids = fields.One2many('ex.sso.app', 'school_ref', u'应用列表')
    class_ids = fields.One2many("ex.base.class", "school_ref", "班级")

    attr_type = fields.Selection([
        ('1', u'托儿所'),
        ('2', u'幼儿园'),
        ('3', u'小学'),
        ('4', u'初中'),
        ('5', u'高中'),
        ('6', u'大学'),
    ], u'学校类别')



class ex_cfg_wechat_cfg(models.Model):
    _name = 'ex.cfg.wechat.cfg'
    _description = u'微信消息通道配置'

    name = fields.Char("name")
    appid = fields.Char("appid")
    appsecret = fields.Char("appsecret")
    encrypt_mode = fields.Char("encrypt_mode", default="normal")
    encoding_aes_key = fields.Char("encoding_aes_key")
    token = fields.Char("token")
    isactive = fields.Boolean("是否有效", default=True)



class ex_cfg_wechat(models.Model):
    _name = 'ex.cfg.wechat'
    _description = u'微信消息通道'

    wx_url = fields.Char("代理服务地址")
    isactive = fields.Boolean("是否有效", default=True)

    stype = fields.Selection([
        (u'01', u'微信服务号'),
        (u'02', u'微信企业号'),
    ], u'认证方式', default='01')


class ex_cfg_sms(models.Model):
    _name = 'ex.cfg.sms'
    _description = u'短信通道'

    name = fields.Char("name")
    isactive = fields.Boolean("是否有效", default=True)









