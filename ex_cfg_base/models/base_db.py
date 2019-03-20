# -*- coding: utf-8 -*-
import logging, datetime
from odoo import api, fields, models
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
import os
_logger = logging.getLogger(__name__)


"""
        主数据平台的意义：对平台所有应用提供统一的用户界面（身份认证）

        通过旗下各个应用将数据进行进一步筛选，将精华存入主数据库

        1) 将分散在各业务模块的精华数据汇总（针对孩子）

        2）建立起家长与孩子的永久关系

        3）建立起教师与孩子的永久关系

        4) 针对家长的权限管理机制

"""

"""
    接口设计

        1、学生
            1.1 注册一个学生，返回创建成功的uid，业务库自己维护该id的业务
            1.2 注销一个学生，根据uid注销一个学生的主数据记录
            1.3 根据学籍号、身份证号码查询学生记录
        注：
            1）学生以学籍号、身份证号码为现实世界的唯一标识，在注册新学生之前可以使用这两个字段进行校验，这样才能保证数据库数据的唯一性

        2、家长
            2.1 注册一个家长，返回创建成功的uid
            2.2 注销一个家长

        3、教师
            3.1 注册一个教师，返回创建成功的uid
            3.2 注销一个教师

        注：
            1）家长和老师以手机号码为主键，注册一个新的用户必须要进过手机号码校验，保证整个数据库用户信息的手机号码键唯一

        4、聚合查询
            4.1 根据uid或电话号码查询家长或老师的索引信息

        注：
            1）聚合查询在api服务中以api接口的形式，暴露给"主功能路由"程序，然后通过token的形式传递给app
            2）app通过聚合查询的结果，使用主数据id通过各自的业务rest方法获取业务数据资源开展业务功能

        5、添加权限
            5.1 注册某个家长的使用权限
            5.2 取消某个家长的使用权限
            5.3 批量注册、取消某权限

        注：
            1、业务app通过业务规则自主注册、取消某个用户的访问权限，并在业务中控制应用的可用与否



"""
######################################################################################################################
#  组织结构
######################################################################################################################
class ex_base_grade(models.Model):
    """
        年级
    """
    _name = 'ex.base.grade'
    _rec_name = 'name'
    _description = u'入学年级'
    _log_access = False

    name = fields.Char("入学年份（YYYY）")

class ex_base_class(models.Model):
    """
        班级
    """
    _name = 'ex.base.class'
    _rec_name = 'displayname'
    _description = u'班级'
    _log_access = False

    name = fields.Char("班级名称")
    grade_ref = fields.Many2one("ex.base.grade", "年级")
    school_ref = fields.Many2one("ex.cfg.school", "学校")

    student_ids = fields.One2many('ex.base.db.student', 'class_ref', u'学生')
    teacher_ids = fields.One2many("ex.base.db.class.teacher.rel", 'class_ref', u'教师')

    isactive = fields.Boolean("是否有效", default=True)

    displayname = fields.Char('显示', compute="_show_name", store=True)


    @api.one
    @api.depends('grade_ref','school_ref','name')
    def _show_name(self):
        """
        根据不同的版本显示不同的年级名称
        :return:
        """

        now = datetime.datetime.now()
        yearstr = now.strftime("%Y")
        se = int(yearstr) - int(self.grade_ref.name)
        _grade = u"%s界" % self.grade_ref.name
        
        if self.school_ref.attr_type == "2" :

            if se == 1:
                _grade = u"小班"
            elif se == 2:
                _grade = u"中班"
            elif se == 3:
                _grade = u"大班"
            else:
                _grade = u"%s界"%self.grade_ref.name
        elif self.school_ref.attr_type == "3" :
            if se == 1:
                _grade = u"一年级"
            elif se == 2:
                _grade = u"二年级"
            elif se == 3:
                _grade = u"三年级"
            elif se == 4:
                _grade = u"四年级"
            elif se == 5:
                _grade = u"五年级"
            elif se == 6:
                _grade = u"六年级"
            else:
                _grade = u"%s界"%self.grade_ref.name

        self.displayname = "%s/%s/%s"%(self.school_ref.fullname, _grade, self.name)

######################################################################################################################
#  学生
######################################################################################################################
class ex_base_db_student(models.Model):
    """
        [每一个现实中的学生产生一条记录]
    """
    _name = 'ex.base.db.student'
    _description = u'学生档案'
    _log_access = False

    name = fields.Char(u"姓名")

    student_sn = fields.Char(u'学籍号')
    identification_id = fields.Char(u'证照号码')
    phone = fields.Char(u'联系电话')
    image_medium = fields.Binary(string=u'头像')

    # -------来自老平台-------
    stu_code = fields.Char('学号')
    openid = fields.Char('openid')
    nick_name = fields.Char('小名')
    birthday = fields.Date('出生年月')
    sex = fields.Selection([
        (1, "男"),
        (2, "女"),
    ], '性别')
    bloodtype = fields.Selection([
        (1, "A型"),
        (2, "B型"),
        (3, "AB型"),
        (4, "O型"),
    ], '血型')
    nation = fields.Char('民族')
    nativeplace = fields.Char('籍贯')
    address = fields.Char('居住地址')
    idcard = fields.Char('身份证号')
    introduce = fields.Text('宝贝介绍')
    allergy = fields.Text('过敏史')
    interest = fields.Text('兴趣爱好')
    remark = fields.Text('备注')

    # ------------------------------------------
    ic_card = fields.Char("IC卡号")

    his_ids = fields.One2many('ex.base.db.student.his', 'student_ref', u'学籍记录')
    parent_ids = fields.One2many('ex.base.db.student.parent.rel', 'student_ref', u'家长列表')
    teacher_ids = fields.One2many('ex.base.db.student.teacher.rel', 'student_ref', u'老师列表')

    # 成长档案、精彩瞬间、荣誉、图文、视频资料
    file_ids = fields.One2many('ex.base.db.file', 'student_ref', u'资料库')
    isactive = fields.Boolean("是否有效", default=True)

    class_ref = fields.Many2one("ex.base.class", "班级")

    write_app = fields.Many2one("ex.sso.app.tpl","写入程序")
    write_time = fields.Datetime("写入时间")

class ex_base_db_student_his(models.Model):
    """
    [每一个学生的每一次入学事件会产生一条记录]

    """
    _name = 'ex.base.db.student.his'
    _description = u'学籍记录'
    _log_access = False

    schoolname = fields.Many2one("ex.cfg.school","学校")
    year = fields.Char('入学年份')

    isactive = fields.Boolean("是否有效", default=True)
    student_ref = fields.Many2one("ex.base.db.student",u"学生")

    write_app = fields.Many2one("ex.sso.app.tpl", "写入程序")
    write_time = fields.Datetime("写入时间")


class ex_base_db_student_parent_rel(models.Model):
    """
    [每一个用户（家长）绑定一个学生后会产生一条关系]
    """
    _name = 'ex.base.db.student.parent.rel'
    _description = u'学生家长关系'
    _log_access = False

    student_ref = fields.Many2one("ex.base.db.student", u"学生")
    parent_ref = fields.Many2one("ex.base.db.parent", u"家长")
    name = fields.Char("关系名称")
    isactive = fields.Boolean("是否有效", default=True)

    write_app = fields.Many2one("ex.sso.app.tpl", "写入程序")
    write_time = fields.Datetime("写入时间")

class ex_base_db_student_teacher_rel(models.Model):
    """
    [每一个用户（教师）绑定一个学生后会产生一条关系]
    """
    _name = 'ex.base.db.student.teacher.rel'
    _description = u'学生教师关系'
    _log_access = False

    student_ref = fields.Many2one("ex.base.db.student", u"学生")
    teacher_ref = fields.Many2one("ex.base.db.teacher", u"教师")
    name = fields.Char("关系名称")
    isactive = fields.Boolean("是否有效", default=True)

    write_app = fields.Many2one("ex.sso.app.tpl", "写入程序")
    write_time = fields.Datetime("写入时间")


class ex_base_db_class_teacher_rel(models.Model):
    """
    教师与班级的关系
    """
    _name = 'ex.base.db.class.teacher.rel'
    _description = u'班级教师关系'
    _log_access = False

    class_ref = fields.Many2one("ex.base.class", u"班级")
    teacher_ref = fields.Many2one("ex.base.db.teacher", u"教师")
    name = fields.Char("关系名称")
    isactive = fields.Boolean("是否有效", default=True)

    write_app = fields.Many2one("ex.sso.app.tpl", "写入程序")
    write_time = fields.Datetime("写入时间")

class ex_base_db_file(models.Model):
    """
        [每一个学生在各个业务模块中发生的精彩瞬间，都会产生一条记录]
    """
    _name = 'ex.base.db.file'
    _description = u'资料'
    _log_access = False

    filetype = fields.Char(u"分类")
    title = fields.Char(u"标题")
    file = fields.Binary(u'文件')

    student_ref = fields.Many2one("ex.base.db.student", u"学生")

    write_app = fields.Many2one("ex.sso.app.tpl","写入程序")
    write_time = fields.Datetime("写入时间")

######################################################################################################################
# 平台用户
######################################################################################################################
class ex_base_db_user(models.Model):
    """
        [可以通过手机、电脑获取平台在线服务的用户]
    """
    _name = 'ex.base.db.user'
    _description = u'平台用户'
    _log_access = False

    # 业务属性
    name = fields.Char(u"姓名")
    gender = fields.Selection([
        ('male', u'男'),
        ('female', u'女')
    ], u'性别')
    identification_id = fields.Char(u'证照号码')
    birthday = fields.Date(u'生日')
    remark = fields.Text(u"备注")
    isactive = fields.Boolean("是否有效", default=True)

    phone = fields.Char(u'手机号码')
    ic_card = fields.Char("IC卡号")

    write_app = fields.Many2one("ex.sso.app.tpl", "写入程序")
    write_time = fields.Datetime("写入时间")


class ex_base_db_parent_wechat_bind(models.Model):
    """
       每一次绑定都会产生一条记录

       每一个用户可以绑定多个微信公众平台
    """
    _name = 'ex.base.db.parent.wechat.bind'
    _description = u'家长微信绑定记录'
    _log_access = False

    wechat_ref = fields.Many2one("ex.cfg.wechat", "微信公众号")
    parent_ref = fields.Many2one("ex.base.db.parent", "家长绑定记录")
    openid = fields.Char("openid")

class ex_base_db_teacher_wechat_bind(models.Model):
    """
       每一次绑定都会产生一条记录

       每一个用户可以绑定多个微信公众平台
    """
    _name = 'ex.base.db.teacher.wechat.bind'
    _description = u'教师微信绑定记录'
    _log_access = False

    wechat_ref = fields.Many2one("ex.cfg.wechat", "微信公众号")
    teacher_ref = fields.Many2one("ex.base.db.teacher", "家长绑定记录")
    openid = fields.Char("openid")

class ex_base_db_parent(models.Model):
    """
        [家长是平台的主要用户]

        平台旗下所有应用可以通过【手机号码】【uid】获取其所有孩子的所有信息

        各个产品的app端家长使用的功能应该都是一致的，所有没有设计角色机制

        针对收费业务设计了权限控制机制
    """
    _name = 'ex.base.db.parent'
    _inherit = ['ex.base.db.user']
    _description = u'家长档案'
    _log_access = False

    auth_ids = fields.One2many("ex.base.db.parent.auth", "parent_ref", "权限控制")
    bind_ids = fields.One2many("ex.base.db.parent.wechat.bind", "parent_ref", "绑定记录")


class ex_base_db_teacher(models.Model):
    """
        [教师是平台的主要用户]

        平台旗下所有应用可以通过【手机号码】【uid】获取其教过的所有孩子的所有信息

        针对一些需要划分角色的应用，设计提供了角色机制

    """
    _name = 'ex.base.db.teacher'
    _inherit = ['ex.base.db.user']
    _description = u'教师档案'
    _log_access = False

    role_ids = fields.One2many("ex.base.db.teacher.role", "teacher_ref", "角色")
    bind_ids = fields.One2many("ex.base.db.teacher.wechat.bind", "teacher_ref", "绑定记录")



######################################################################################################################
# 应用辅助
######################################################################################################################

class ex_base_db_parent_auth(models.Model):
    """
         [每一个教师创建档案的时候会创建]
    """
    _name = 'ex.base.db.parent.auth'
    _description = u'功能权限'
    _log_access = False

    key = fields.Char(u"key", related="name.key")
    name = fields.Many2one("ex.base.key", "名称", domain="[('isactive','=',True)]")
    expired_date = fields.Date("过期日期")

    parent_ref = fields.Many2one("ex.base.db.parent", "家长")

    write_app = fields.Many2one("ex.sso.app.tpl", "写入程序")
    write_time = fields.Datetime("写入时间")
    isactive = fields.Boolean("是否有效", default=True)


class ex_base_db_teacher_role(models.Model):
    """
         [应用可以根据需要管理用户的角色机制]
    """
    _name = 'ex.base.db.teacher.role'
    _description = u'应用角色'
    _log_access = False

    key = fields.Char(u"key", related="name.key")
    name = fields.Many2one("ex.base.key", "名称", domain="[('isactive','=',True)]")
    teacher_ref = fields.Many2one("ex.base.db.teacher", "教师")

    write_app = fields.Many2one("ex.sso.app.tpl", "写入程序")
    write_time = fields.Datetime("写入时间")
    isactive = fields.Boolean("是否有效", default=True)


class ex_base_key(models.Model):
    """

    """
    _name = 'ex.base.key'
    _rec_name = 'name'
    _description = u'key字典'
    _log_access = False

    key = fields.Char(u"key")
    name = fields.Char(u"名称")
    remark = fields.Text(u"备注")

    write_app = fields.Many2one("ex.sso.app.tpl", "写入程序")
    write_time = fields.Datetime("写入时间")
    isactive = fields.Boolean("是否有效", default=True)