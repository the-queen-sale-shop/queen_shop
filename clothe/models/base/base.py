# -*- coding: utf-8 -*-
import logging, datetime
from odoo import api, fields, models,exceptions
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
import os,json,urllib2,traceback,logging
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


#小阿萍
class trade_people(models.Model):
    """
        顾客
    """
    _name = 'trade.people'
    _rec_name = 'name'
    _description = u'顾客'

    name = fields.Char("顾客姓名", required=True)
    phone = fields.Char("联系方式")
    birthday = fields.Date("顾客生日")
    score = fields.Float("积分")
    trade_num = fields.Integer("消费笔数")
    order_ids = fields.One2many('trade.order', 'people_ref', '订单详情')
    total = fields.Float("消费汇总",compute='_get_total',store=True)
    profit = fields.Float("利润合计",compute='_get_profit',store=True)

    #计算顾客消费合计
    @api.one
    @api.depends('order_ids.total')
    def _get_total(self):
        self.total = sum(item.total for item in self.order_ids)

    # 计算利润合计
    @api.one
    @api.depends('order_ids.profit')
    def _get_profit(self):
        self.profit = sum(item.profit for item in self.order_ids)



class trade_order(models.Model):
    """
        订单
    """
    _name = 'trade.order'
    _rec_name = 'name'
    _description = u'订单'

    name = fields.Char("订单名称", readonly=True)
    people_ref = fields.Many2one("trade.people", "顾客", required=True)
    trade_time = fields.Datetime("消费时间", readonly=True)
    item_ids = fields.One2many('trade.order.item', 'order_ref', '订单明细')
    total = fields.Float("订单销售金额",compute='_get_total', store=True)
    cost = fields.Float("订单成本",compute='_get_cost', store=True)
    rate_ref = fields.Many2one("trade.dis.rate", "折扣率",required=True)
    discount = fields.Float("折后优惠金额", default=0)
    profit = fields.Float("单笔订单利润",compute='_get_oo_profit', store=True)
    sale = fields.Char("销售人")

    #重写方法删除订单
    @api.multi
    def unlink(self):
        super(trade_order_item, self.item_ids).unlink()
        super(trade_order,self).unlink()

    #生成订单号、时间
    @api.model
    def create(self, vals):
        t_name = str(datetime.datetime.now())[0:18].replace('-','').replace(':','').replace(' ','')
        t_time = datetime.datetime.now()
        vals['name'] = 'nw'+t_name
        vals['trade_time'] = t_time
        result = super(trade_order, self).create(vals)
        return result


    #计算售价
    @api.one
    @api.depends('item_ids.price_sell','item_ids.num','discount','rate_ref.dis_rate')
    def _get_total(self):
        self.total = sum((item.price_sell)*(item.num) for item in self.item_ids)*self.rate_ref.dis_rate-self.discount

    # 计算成本
    @api.one
    @api.depends('item_ids.price_cost', 'item_ids.num')
    def _get_cost(self):
        self.cost = sum((item.price_cost)*(item.num) for item in self.item_ids)

    # 计算利润
    @api.one
    @api.depends('discount','item_ids.price_sell', 'item_ids.price_cost', 'item_ids.num','rate_ref.dis_rate')
    def _get_oo_profit(self):
        self.profit = sum((item.price_sell)*(item.num) for item in self.item_ids)*self.rate_ref.dis_rate-self.discount - sum((item.price_cost)*(item.num) for item in self.item_ids)


# class res_users(models.Model):
#     """
#         工作人员
#     """
#     _inherit = 'res.users'
#
#     name = fields.Char("工作人员姓名")
#     passwd = fields.Char("登入密码")


class trade_order_item(models.Model):
    """
        订单明细
    """
    _name = 'trade.order.item'
    _rec_name = 'stock_ref'
    _description = u'订单明细'

    order_ref = fields.Many2one("trade.order", "所属订单")
    stock_ref = fields.Many2one("trade.stock", "单品")
    another_name = fields.Char("别名",related='stock_ref.another_name', store=True)
    price_sell = fields.Float("销售单价",related='stock_ref.price_sell', store=True)
    price_cost = fields.Float("成本",related='stock_ref.price_cost', store=True)
    num = fields.Integer("购买数量", default=1)
    total = fields.Float("单品销售合计",compute='_get_ii_total',store=True)
    profit = fields.Float("单品利润",compute='_get_ii_profit', store=True)

    #计算单品售价
    @api.one
    @api.depends('price_sell', 'num')
    def _get_ii_total(self):
        self.total = (self.price_sell) * self.num

    # 计算单品利润
    @api.one
    @api.depends('price_sell', 'price_cost','num')
    def _get_ii_profit(self):
        self.profit = (self.price_sell-self.price_cost) * self.num




class trade_stock(models.Model):
    """
     库存
    """
    _name = 'trade.stock'
    _rec_name = 'name'
    _description = u'库存'

    name = fields.Char("商品名称")
    another_name = fields.Char("别名")
    price_cost = fields.Float("进价")
    total_num = fields.Integer("总库存")
    num = fields.Integer("库存数量",compute='_get_num',store=True)
    cost_total = fields.Float("库存金额",compute='_get_total',store=True)
    price_sell = fields.Float("售价")
    order_item_ids = fields.One2many('trade.order.item', 'stock_ref', '订单明细')
    intime = fields.Datetime("进货时间", readonly=True)

    #计算库存金额
    @api.one
    @api.depends('price_cost', 'num')
    def _get_total(self):
        kk= self.cost_total
        self.cost_total = self.price_cost * self.num

    # 计算库存数量
    @api.one
    @api.depends('order_item_ids.num','total_num')
    # @api.onchange('num')
    def _get_num(self):
        kk = 0
        self.num = self.total_num - sum(line.num for line in (self.order_item_ids))

    # 生成订单号、时间
    @api.model
    def create(self, vals):
        t_time = datetime.datetime.now()
        vals['intime'] = t_time
        result = super(trade_stock, self).create(vals)
        return result


class trade_dis_rate(models.Model):
    """
        折扣表
    """
    _name = 'trade.dis.rate'
    _rec_name = 'dis_rate'
    _description = u'折扣表'

    dis_rate = fields.Float("折扣率")




