## 搭建属于自己的微信推送服务，完美替代server酱、wxpusher等。保护隐私


+ 注册企业微信：参考教程，这里不再赘述

>https://jingyan.baidu.com/article/2c8c281d65dc670009252a57.html



+ 注册好企业微信（https://work.weixin.qq.com/）

+ 进入管理后台-->选择应用管理-->选择创建应用-->填写应用名称

+ 创建好后，得到 AgentId 和 Secret 两个值

+ 回到企业微信后台，选择我的企业，翻到最底下，得到企业 ID

  这些参数后面会用到！

  

  ```
  参考了官方文档：https://work.weixin.qq.com/api/doc/90001/90143/90372 
  里面列出了所有类型的消息发送请求类型以及参数
  ```

  

**以文本消息为例：**

```
请求方式：POST（HTTPS）
请求地址： https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN
```

参数：

    {
    "touser" : "UserID1|UserID2|UserID3",
    "toparty" : "PartyID1|PartyID2",
    "totag" : "TagID1 | TagID2",
    "msgtype" : "text",
    "agentid" : 1,
    "text" : {
        "content" : "你的快递已到，请携带工卡前往邮件中心领取。/n出发前可查看<a href=/"http://work.weixin.qq.com/">邮件中心视频实况</a>，聪明避开排队。"
    },
    "safe":0,
    "enable_id_trans": 0,
    "enable_duplicate_check": 0,
    "duplicate_check_interval": 1800
    }

参数说明：

![1](/img/1.png)

> touser、toparty、totag不能同时为空，后面不再强调。



**哪些是发送消息方法需要的“变量”？**

|     参数     | 说明                                                         |
| :----------: | :----------------------------------------------------------- |
| access_token | 调用接口凭证                                                 |
|   agentid    | 企业应用的id，整型。企业内部开发，可在应用的设置页面查看；第三方服务商，可通过接口 获取企业授权信息 获取该参数值 |


​	![2](/img/2.png)



至此，我们就可以利用写一个Python函数：

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


​    
    #测试
    wxpush('test','@all')

返回参数：

![3](/img/3.png)



手机界面：



![4](/img/4.jpg)





图5：

![5](/img/5.png)

教程至此结束，完整demo代码见demo.py，代码很粗糙，你可以进照猫画虎，开发图文、卡片等诸多类型的消息