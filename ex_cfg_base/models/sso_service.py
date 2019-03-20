# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
import os
import json,urllib2
_logger = logging.getLogger(__name__)

class ex_sso_app(models.Model):
    _name = 'ex.sso.app.tpl'
    _description = u'app应用模板'

    name = fields.Char("名称")
    # 通过身份认证之后，平台把token通过http参数传入此URL
    url = fields.Char("前端url")
    appsecret = fields.Char("appsecret")
    isactive = fields.Boolean("是否有效", default=True)



class ex_sso_school_app(models.Model):
    _name = 'ex.sso.app'
    _description = u'app应用'

    tpl_ref = fields.Many2one("ex.sso.app.tpl","app模板")
    school_ref = fields.Many2one("ex.cfg.school","所属学校")
    isactive = fields.Boolean("是否有效", default=True)

    base_url = fields.Char("统一URL", compute="_base_url", store=True)

    @api.one
    @api.depends('school_ref', 'tpl_ref', 'base_url')
    def _base_url(self):
        """
        统一认证app路由
        api服务通过ex.cfg.school中的微信认证方式查询【主数据聚合索引】生产token
        然后发送重定向到app的指令到客户端
        :return:
        """
        api_host = os.environ["APIHOST"]
        self.base_url = "%s/s/%s/%s"%(api_host, self.school_ref.servicename, self.tpl_ref.id)







