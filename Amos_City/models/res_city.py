# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Odoo Connector
# QQ:35350428
# 邮件:sale@100china.cn
# 手机：13584935775
# 作者：'wangguangjian'
# 公司网址： www.odoo.pw  www.100china.cn
# Copyright 昆山一百计算机有限公司 2012-2016 Amos
# 日期：2014-06-18
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&


from odoo import fields, models, api, _
from datetime import timedelta
from makePinyin import pinyinQuan, pinyinAbbr
from makePinyin import makePinyin


class res_city(models.Model):
    _name = "res.city"
    _description = u"市"
    _order = 'code'

    name = fields.Char(string=u'市', size=64, index=True, default=u'/', required=True, copy=False, )
    code = fields.Char(string=u'邮政编码', copy=False, )
    license_plate = fields.Char(string=u'车牌号码', copy=False, )
    a_z = fields.Char(string=u'首字母', copy=False, )
    spelling = fields.Char(string=u'全拼', copy=False, )
    country_id = fields.Many2one('res.country.state', string=u"省", index=True)
    b_x = fields.Char(string=u'百度X')
    b_y = fields.Char(string=u'百度Y')
    b_active = fields.Boolean(string=u'是否已定位', default=False)

    @api.model
    def create(self, values):
        values['a_z'] = pinyinAbbr(values['name'])[0][0]
        values['spelling'] = pinyinQuan(values['name'], sep="", zhuyin=False, dyz=False)[0]
        line = super(res_city, self).create(values)
        return line


class res_area(models.Model):
    _name = "res.area"
    _description = u"区"
    _order = 'code'

    name = fields.Char(string=u'市', size=64, index=True, default=u'/', required=True, copy=False, )
    code = fields.Char(string=u'编号', copy=False, )
    a_z = fields.Char(string=u'首字母', copy=False, )
    spelling = fields.Char(string=u'全拼', copy=False, )
    zip = fields.Char(string=u'邮编', copy=False, )

    country_id = fields.Many2one('res.city', string=u"市", index=True)
    b_x = fields.Char(string=u'百度X')
    b_y = fields.Char(string=u'百度Y')
    b_active = fields.Boolean(string=u'是否已定位', default=False)

    @api.model
    def create(self, values):
        values['a_z'] = pinyinAbbr(values['name'])[0][0]
        values['spelling'] = pinyinQuan(values['name'], sep="", zhuyin=False, dyz=False)[0]
        line = super(res_area, self).create(values)
        return line


class res_country(models.Model):
    _inherit = 'res.country'

    a_z = fields.Char(string=u'首字母', copy=False, )
    spelling = fields.Char(string=u'全拼', copy=False, )
    b_x = fields.Char(string=u'百度X')
    b_y = fields.Char(string=u'百度Y')
    b_active = fields.Boolean(string=u'是否已定位', default=False)

    @api.model
    def create(self, values):
        values['a_z'] = pinyinAbbr(values['name'])[0][0]
        values['spelling'] = pinyinQuan(values['name'], sep="", zhuyin=False, dyz=False)[0]
        line = super(res_country, self).create(values)
        return line


class res_country_state(models.Model):
    _inherit = 'res.country.state'

    a_z = fields.Char(string=u'首字母', copy=False, )
    spelling = fields.Char(string=u'全拼', copy=False, )
    b_x = fields.Char(string=u'百度X')
    b_y = fields.Char(string=u'百度Y')
    b_active = fields.Boolean(string=u'是否已定位', default=False)

    @api.model
    def create(self, values):
        values['a_z'] = pinyinAbbr(values['name'])[0][0]
        values['spelling'] = pinyinQuan(values['name'], sep="", zhuyin=False, dyz=False)[0]
        line = super(res_country_state, self).create(values)
        return line



