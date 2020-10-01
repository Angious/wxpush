# -*- codeing = utf-8 -*-
# @Author: Angious
# @Time : 2020/5/6 21:05
# @File : demo.py
# @Software : PyCharm

import requests
import json


class WXPusher:
    def __init__(self, usr, msg):
        self.base_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
        self.req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
        self.corpid = 'xxxxxxxxx'     # 上面提到的你的企业ID
        self.corpsecret = '_61bxxxxxxxxxxxxxx'     # 上图的Secret
        self.agentid = 123456          # 填写你的企业ID，不加引号，是个整型常数,就是上图的AgentId
        self.usr = usr
        self.msg = msg

    def get_access_token(self):
        urls = self.base_url + 'corpid=' + self.corpid + '&corpsecret=' + self.corpsecret
        resp = requests.get(urls).json()
        access_token = resp['access_token']
        return access_token

    def send_message(self):
        data = self.get_message()
        req_urls = self.req_url + self.get_access_token()
        res = requests.post(url=req_urls, data=data)
        print(res.text)

    def get_message(self):
        data = {
            "touser": self.usr,
            "toparty": "@all",
            "totag": "@all",
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": self.msg
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        data = json.dumps(data)
        return data


if __name__ == '__main__':
    test = WXPusher(usr='Chenxxx', msg="test")       # usr参数为推送用户名，msg为消息文本
    test.send_message()


