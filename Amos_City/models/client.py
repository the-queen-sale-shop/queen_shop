# -*- coding: utf-8 -*-
# #############################################################################
# WENS FARM BID INFO
# Copyright 2014 WENS Wiexin
# amos
# #############################################################################

import time
import requests
import time
from HTMLParser import HTMLParser
from requests.compat import json as _json

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


class Client(object):
    """
    API 操作类
    通过这个类可以方便的通过钉钉 API 进行一系列操作，比如主动发送消息、创建自定义菜单等
    """

    def __init__(self, corpid=None, corpsecret=None, access_token=None):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.access_token = access_token

    def request(self, method, url, **kwargs):
        if "params" not in kwargs:
            kwargs["params"] = {"access_token": self.access_token}
        if isinstance(kwargs.get("data", ""), dict):
            body = _json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode('utf8')
            kwargs["data"] = body

        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()
        json = r.json()
        return json

    def get(self, url, **kwargs):
        return self.request(
            method="get",
            url=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self.request(
            method="post",
            url=url,
            **kwargs
        )

    def grant_token(self):
        """
        获取 Access Token 。
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/gettoken?",
            params={
                "corpid": self.corpid,
                "corpsecret": self.corpsecret,
            }
        )

    def department_list(self):
        """
        获取 获取部门列表 。
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/department/list?",
            params={
                "access_token": self.access_token,
            }
        )

    def department_get(self, id):
        """
        获取 获取部门详情 。
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/department/get?",
            params={
                "access_token": self.access_token,
                "id": id,
            }
        )

    def department_create(self, param, access_token):
        """
        创建部门。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/department/create?",
            data=param,
            headers={'Content-Type': 'application/json'}
        )

    def department_update(self, param, access_token):
        """
        更新部门。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/department/update?",
            data=param,
            headers={'Content-Type': 'application/json'}
        )

    def department_delete(self, id):
        """
        获取 Access Token 。
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/department/delete?",
            params={
                "access_token": self.access_token,
                "id": id,
            }
        )

    def user_getUseridByUnionid(self, unionid):
        """
        获取 根据unionid获取成员的userid 。
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/user/getUseridByUnionid?",
            params={
                "access_token": self.access_token,
                "unionid": unionid,
            }
        )

    def user_get(self, userid):
        """
        获取 获取成员详情
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/user/get?",
            params={
                "access_token": self.access_token,
                "userid": userid,
            }
        )

    def user_create(self, param, access_token):
        """
        创建员工
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/user/create?",
            data=param,
            headers={'Content-Type': 'application/json'}
        )

    def user_update(self, param, access_token):
        """
        更新成员。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/user/update?",
            data=param,
            headers={'Content-Type': 'application/json'}
        )

    def user_delete(self, userid):
        """
        删除成员
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/user/delete?",
            params={
                "access_token": self.access_token,
                "userid": userid,
            }
        )

    def user_batchdelete(self, useridlist, access_token):
        """
        批量删除成员。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/user/batchdelete?",
            data=useridlist,
            headers={'Content-Type': 'application/json'}
        )

    def user_list(self, department_id):
        """
        获取 获取部门成员（详情）
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/user/list?",
            params={
                "access_token": self.access_token,
                "department_id": department_id,
            }
        )

    def user_simplelist(self, department_id):
        """
        获取 获取部门成员
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/user/simplelist?",
            params={
                "access_token": self.access_token,
                "department_id": department_id,
            }
        )

    def user_get_admin(self):
        """
        获取 获取管理员列表（详情）
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/user/get_admin?",
            params={
                "access_token": self.access_token,
            }
        )

    #::::::::::::::::创建微应用


    def microapp_create(self, data, access_token):
        """
        创建微应用。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/microapp/create?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    def microapp_visible_scopes(self, data, access_token):
        """
        获取企业设置的微应用可见范围。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/microapp/visible_scopes?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    def microapp_set_visible_scopes(self, data, access_token):
        """
        设置微应用的可见范围。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/microapp/set_visible_scopes?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    #::::::::::::::::创建微应用

    def microapp_rule_get_rule_list(self, data, access_token):
        """
        获取指定微应用下指定用户绑定的全部规则。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/microapp/rule/get_rule_list?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    def microapp_rule_get_user_total(self, data, access_token):
        """
        获取规则绑定的用户数。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/microapp/rule/get_user_total?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    def microapp_rule_delete(self, data, access_token):
        """
        删除规则。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/microapp/rule/delete?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    #::::::::::::::::群会话接口


    def chat_create(self, data, access_token):
        """
        创建会话。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/chat/create?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    def chat_update(self, data, access_token):
        """
        修改会话。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/chat/update?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    def chat_get(self, chatid):
        """
        获取会话
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/chat/get?",
            params={
                "access_token": self.access_token,
                "chatid": chatid,
            }
        )

    def chat_bind(self, chatid, agentid):
        """
        绑定微应用和群会话
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/chat/bind?",
            params={
                "access_token": self.access_token,
                "chatid": chatid,
                "agentid": agentid,
            }
        )

    def chat_unbind(self, chatid, agentid):
        """
        解绑微应用和群会话
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/chat/unbind?",
            params={
                "access_token": self.access_token,
                "chatid": chatid,
                "agentid": agentid,
            }
        )

    def chat_send(self, data, access_token):
        """
        发送消息到群会话。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/chat/send?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    #::::::::::::::::普通会话消息接口

    def message_send_to_conversation(self, data, access_token):
        """
        发送消息到群会话。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/message/send_to_conversation?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    #::::::::::::::::企业会话消息接口

    def message_send(self, data, access_token):
        """
        发送企业会话消息。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/message/send?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    def message_list_message_status(self, data, access_token):
        """
        获取企业会话消息已读未读状态。
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/message/list_message_status?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    #::::::::::::::::管理多媒体文件


    def media_upload(self, data, access_token):
        """
        上传媒体文件。上传的媒体文件限制

                图片（image）:1MB，支持JPG格式
                语音（voice）：2MB，播放长度不超过60s，AMR格式
                普通文件（file）：10MB

        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/media/upload?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    def media_get(self, media_id):
        """
        获取媒体文件 通过media_id获取图片、语音等文件。
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/media/get?",
            params={
                "access_token": self.access_token,
                "media_id": media_id,
            }
        )

    #::::::::::::::::获取企业员工人数

    def user_get_org_user_count(self, onlyActive):
        """
        获取媒体文件 通过media_id获取图片、语音等文件。
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/user/get_org_user_count?",
            params={
                "access_token": self.access_token,
                "onlyActive": onlyActive,
            }
        )

    #::::::::::::::::钉盘接口API

    def cspace_add_to_single_chat(self, data, access_token):
        """
        发送文件给指定用户
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/cspace/add_to_single_chat?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

    def cspace_add(self, agent_id, code, media_id, space_id, folder_id, name, overwrite):
        """
        新增文件到用户钉盘
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/cspace/add?",
            params={
                "access_token": self.access_token,
                "agent_id": agent_id,
                "code": code,
                "media_id": media_id,
                "space_id": space_id,
                "folder_id": folder_id,
                "name": name,
                "overwrite": overwrite,
            }
        )

    def cspace_get_custom_space(self, domain, agent_id):
        """
        获取企业下的自定义空间
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/cspace/get_custom_space?",
            params={
                "access_token": self.access_token,
                "domain": domain,
                "agent_id": agent_id,
            }
        )

    def cspace_grant_custom_space(self, agent_id, domain, type, userid, path, fileids, duration):
        """
        获取企业下的自定义空间
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/cspace/grant_custom_space?",
            params={
                "access_token": self.access_token,
                "agent_id": agent_id,
                "domain": domain,
                "type": type,
                "userid": userid,
                "path": path,
                "fileids": fileids,
                "duration": duration,
            }
        )

    def cspace_get_download_key(self, agent_id, code, dentry_id, space_id):
        """
        获取文件下载key 获取钉盘文件下载的key，key7天内有效
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/cspace/get_download_key?",
            params={
                "access_token": self.access_token,
                "agent_id": agent_id,
                "code": code,
                "dentry_id": dentry_id,
                "space_id": space_id,
            }
        )

    def file_download_by_key(self, agent_id, download_key):
        """
        下载钉盘文件
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/file/download_by_key?",
            params={
                "access_token": self.access_token,
                "agent_id": agent_id,
                "download_key": download_key,
            }
        )

    def file_download_by_key(self, agent_id, file_size,chunk_numbers):
        """
        开启文件上传事务 文件分块上传第一步，开启上传事务，该接口返回upload_id，分块最小需大于100KB，最大不超过8M，最多支持10000块
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/file/upload/transaction?",
            params={
                "access_token": self.access_token,
                "agent_id": agent_id,
                "file_size": file_size,
                "chunk_numbers": chunk_numbers,
            }
        )

    def file_upload_chunk(self, data, access_token):
        """
        上传文件块 文件分块上传中间环节，传输文件块，除最后一块外每块的大小不得小于100KB，最大不超过超过8M，使用标准 http multipart 上传
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/file/upload/chunk?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )


    def file_upload_transaction(self, agent_id, file_size,chunk_numbers,upload_id):
        """
        提交文件上传事务 文件分块上传最后一步，提交本次分块上传事务，默认情况下，系统会删除超过 24 小时没有提交的分块文件上传事务
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/file/upload/transaction?",
            params={
                "access_token": self.access_token,
                "agent_id": agent_id,
                "file_size": file_size,
                "chunk_numbers": chunk_numbers,
                "upload_id": upload_id,
            }
        )


    def file_upload_single(self, data, access_token):
        """
        单步文件上传  单步文件上传，标准 http multipart 上传，文件大小不得超过8M
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/file/upload/single?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

#::::::::::::::::免登

    def user_getuserinfo(self, code):
        """
        通过CODE换取用户身份 企业应用的服务器在拿到CODE后，需要将CODE发送到钉钉开放平台接口，如果验证通过，则返回CODE对应的用户信息。**此接口只用于免登服务中用来换取用户信息**
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/user/getuserinfo?",
            params={
                "access_token": self.access_token,
                "code": code,
            }
        )

    def sso_getuserinfo(self, code):
        """
        通过CODE换取微应用管理员的身份信息 企业应用的服务器在拿到CODE后，需要将CODE发送到钉钉开放平台接口，如果验证通过，则返回CODE对应的管理员信息。**此接口只用于微应用后台管理员免登中用来换取管理员信息
        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/sso/getuserinfo?",
            params={
                "access_token": self.access_token,
                "code": code,
            }
        )

#::::::::::::::::普通钉钉用户账号开放

    def sso_gettoken(self, appid,appsecret):
        """
        普通钉钉用户账号开放相关接口和企业应用开发、ISV应用开发无关，第三方web服务提供商取得钉钉开放应用的appid及appsecret后，可以获取开放应用的ACCESS_TOKEN        :return: 返回的 JSON 数据包
        """
        return self.get(
            url="https://oapi.dingtalk.com/sns/gettoken?",
            params={
                "appid": appid,
                "appsecret": appsecret,
            }
        )


    def sns_get_persistent_code(self, data, access_token):
        """
        获取用户授权的持久授权码
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/sns/get_persistent_code?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )


    def sns_get_sns_token(self, data, access_token):
        """
        获取用户授权的SNS_TOKEN
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/sns/get_sns_token?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )


    def sns_getuserinfo(self, sns_token):
        """
        获取用户授权的个人信息
        """
        return self.get(
            url="https://oapi.dingtalk.com/sns/getuserinfo?",
            params={
                "sns_token": sns_token,
            }
        )

#::::::::::::::::考勤打卡数据开放

    def attendance_list(self, data, access_token):
        """
        考勤打卡数据开放
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/attendance/list?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

#::::::::::::::::统计数据

    def data_record(self, data, access_token):
        """
        考勤打卡数据开放
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/data/record?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )


    def data_update(self, data, access_token):
        """
        isv企业可以通过这个接口更新微应用数据，所更新的数据必须是通过/data/record接口插入的，现在只能更新module，callbackUrl，extension三个字段
        :return: 返回的 JSON 数据包
        """
        self.access_token = access_token
        return self.post(
            url="https://oapi.dingtalk.com/data/update?",
            data=data,
            headers={'Content-Type': 'application/json'}
        )






