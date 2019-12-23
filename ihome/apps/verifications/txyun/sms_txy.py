from qcloudsms_py import QcloudSms

def Sms_txy(mobile,datas):
    # 短信应用 SDK AppID
    appid = 1400289689
    # 短信应用 SDK AppKey
    appkey = "d76635b5cdd68508c642b194e6658691"
    # 需要发送短信的手机号码
    phone_numbers = [mobile]
    # 短信模板ID，
    template_id = 479797
    # 签名
    sms_sign = "mourner"
    # 内容
    params = [datas]  # 当模板没有参数时，`params = []`

    qcloudsms = QcloudSms(appid, appkey)
    # 创建对象
    ssender = qcloudsms.SmsSingleSender()
    # 发送短信
    result = ssender.send_with_param(86, phone_numbers[0],template_id, params, sign=sms_sign, extend="", ext="")
    print(result)

