#-*- codeing = utf-8 -*-
#@Author: Angious
#@Time : 2020/5/6 21:05
#@File : demo.py
#@Software : PyCharm

import requests
import json

wxpush_usr = '你的ID，英文的，你可以如图5.png画出来的那个'

def wxpush(msg,usr):
    base_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
    req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
    corpid = '上面提到的你的企业ID，'
    corpsecret = '上图的Secret'
    
    #获取access_token，每次的access_token都不一样，所以需要运行一次请求一次
    def get_access_token(base_url, corpid, corpsecret):
        urls = base_url + 'corpid=' + corpid + '8&corpsecret=' + corpsecret
        resp = requests.get(urls).json()
        access_token = resp['access_token']
        return access_token

    def send_message(msg, usr):
        data = get_message(msg, usr)
        req_urls = req_url + get_access_token(base_url, corpid, corpsecret)
        res = requests.post(url=req_urls, data=data)
        print(res.text)

    def get_message(msg, usr):
        data = {
            "touser": usr,
            "toparty": "@all",
            "totag": "@all",
            "msgtype": "text",
            "agentid": 填写你的企业ID，不加引号，是个整型常数,就是上图的AgentId
            "text": {
                "content": msg
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        data = json.dumps(data)
        return data

    msg = msg
    usr = usr
    send_message(msg, usr)


#测试
wxpush('test','@all')

