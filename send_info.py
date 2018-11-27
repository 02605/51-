# -*- coding: utf-8 -*-
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""
class SendMessage:
    def __init__(self):
        self.REGION = "cn-hangzhou"
        self.PRODUCT_NAME = "Dysmsapi"
        self.DOMAIN = "dysmsapi.aliyuncs.com"
        self.ACCESS_KEY_ID = "" # self_key_id
        self.ACCESS_KEY_SECRET = "" # self_pwd

        self.acs_client = AcsClient(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET, self.REGION)
        region_provider.add_endpoint(self.PRODUCT_NAME, self.REGION, self.DOMAIN)

    def send_sms(self, business_id, phone_numbers, sign_name, template_code, template_param=None):
        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(template_code)

        # 短信模板变量参数
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)

        # 设置业务请求流水号，必填。
        smsRequest.set_OutId(business_id)

        # 短信签名
        smsRequest.set_SignName(sign_name)

        # 数据提交方式
        # smsRequest.set_method(MT.POST)

        # 数据提交格式
        # smsRequest.set_accept_format(FT.JSON)

        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_numbers)

        # 调用短信发送接口，返回json
        smsResponse = self.acs_client.do_action_with_exception(smsRequest)

        # TODO 业务处理

        return smsResponse

    def test_send(self, my_dicts, mode_code):
        for key in my_dicts.keys():
            params = "{\"name\":\""+key+"\",\"holiady\":\"fantabulous\"}"
            #params = u'{"name":'+key+',"holiady":"冬至"}'
            business_id = uuid.uuid1()
            print(self.send_sms(business_id, my_dicts[key], "Fantabulous", mode_code, params))


if __name__ == '__main__':
    my_dicts = {"任旭": "18531655801"}
    Send = SendMessage()
    Send.test_send(my_dicts, "SMS_150736399")
    
    # test_send(my_dicts, "SMS_150736399")

   
    
    

