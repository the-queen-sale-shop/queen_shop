# -*- coding: utf-8 -*-

from odoo import tools,api
from odoo import models, fields


class trade_report(models.Model):
    """
        销售报表
    """
    _name = 'trade.report'
    _rec_name = 'name'
    _description = u'销售报表'

    name = fields.Char("订单名称")
    people_ref = fields.Char("顾客")
    trade_time = fields.Datetime("消费时间")
    total = fields.Float("订单销售金额")
    cost = fields.Float("订单成本")
    profit = fields.Float("订单利润")
    sale = fields.Char("销售人")

    @api.multi
    def get_myreport(self):
        view = self.env.ref('clothe.view_report_tree')
        sql = "delete from trade_report"
        self.env.cr.execute(sql)

        sql = """
        select tt.name,pp.name as people_ref,tt.trade_time,tt.total,tt.cost,tt.profit,tt.sale from trade_order tt 
        left join trade_people pp on tt.people_ref=pp.id order by tt.id desc
        """
        self._cr.execute(sql)
        row = self.env.cr.fetchall()
        for r in row:
            _data = {
                "name": r[0],
                "people_ref": r[1],
                "trade_time": r[2],
                "total": r[3],
                "cost": r[4],
                "profit": r[5],
                "sale": r[6],
            }
            sql = "insert into trade_report(name,people_ref,trade_time,total,cost,profit,sale)" \
                  "values(%(name)s,%(people_ref)s,%(trade_time)s,%(total)s,%(cost)s,%(profit)s,%(sale)s)"
            self.env.cr.execute(sql, _data)

        view_g = self.env.ref('clothe.view_report_graph')
        view_p = self.env.ref('clothe.view_report_pivot')
        return {
            'name': u'销售报表统计',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'trade.report',
            'view_id': False,
            'views': [(view.id, 'tree'),(view_p.id, 'pivot'),(view_g.id, 'graph')],
            'limit': 65535,
            'type': 'ir.actions.act_window',
            #'domain': domain_data
        }