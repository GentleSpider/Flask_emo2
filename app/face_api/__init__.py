# !codeing: utf-8
# 创建百度云人脸识别客户端
from aip import AipFace

""" 你的 APPID AK SK """
APP_ID = '14575463'
API_KEY = 'Yt3NpnpNVGDorUd1ZyGcI2aC'
SECRET_KEY = 'AzcyDbBwpVGD5cAtyUWYMTKfuiGhvxHQ'

baidu_client = AipFace(APP_ID, API_KEY, SECRET_KEY)


# 初始化邮箱客户端
import smtplib
import traceback
email_sender = '497544867@qq.com'
check_code = 'hgbsgyaieywxcbee'
def email_server_init():
    try:
        email_server = smtplib.SMTP("smtp.qq.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
        email_server.login(email_sender, check_code)  # 括号中对应的是发件人邮箱账号、邮箱密码
    except:
        traceback.print_exc();
        return None
    return email_server

email_server = email_server_init()
