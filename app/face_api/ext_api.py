

def baidu_emo_api(image_in, imageType_in):
    '''

    :param image: 输入的图片可以为face_token 也可以为base64
    :param imageType:  BASE64或者FACE_TOKEN  COMPARE_RES
    :return:
    '''
    from . import baidu_client
    # imageType = "BASE64"
    # imageType = 'FACE_TOKEN'

    if imageType_in == 'COMPARE_RES':
        image = image_in['result']['face_list'][1]['face_token']
        imageType = 'FACE_TOKEN'
    else:
        image = image_in
        imageType = imageType_in

    """ 如果有可选参数 """
    options = {}
    options["face_field"] = "emotion"
    # options["max_face_num"] = 2
    # options["face_type"] = "LIVE"

    """ 带参数调用人脸检测 """
    res = baidu_client.detect(image, imageType, options)
    res_emo = res['result']['face_list'][0]['emotion']['type']
    return res_emo

def py3_warn_mail(reciver, warning_name):
    '''
    用来发送email
    :param reciver:  接收邮件的邮箱
    :param warning_name: 出现危险者的姓名 在邮件内容中显示
    :return: 发送成功返回true 否则false
    '''
    # coding:utf-8   #强制使用utf-8编码格式
    import smtplib  # 加载smtplib模块
    from email.mime.text import MIMEText
    from email.utils import formataddr
    import traceback
    my_sender = '497544867@qq.com'  # 发件人邮箱账号，为了后面易于维护，所以写成了变量
    my_user = reciver  # 收件人邮箱账号，为了后面易于维护，所以写成了变量
    msg_send = u'你的朋友'+warning_name+'可能正处于危险'
    ret = True
    try:
        msg = MIMEText(msg_send, 'plain', 'utf-8')
        msg['From'] = formataddr([u"警告员", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = u"警告"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP("smtp.qq.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, "hgbsgyaieywxcbee")  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 这句是关闭连接的意思
    except Exception as e:  # 如果try中的语句没有执行，则会执行下面的ret=False
        ret = False
        traceback.print_exc()
    return ret

def py3_warn_mail_with_exist_server(reciver, warning_name):
    from email.mime.text import MIMEText
    from email.utils import formataddr
    import traceback
    from app.face_api import email_sender,email_server
    my_user = reciver  # 收件人邮箱账号，为了后面易于维护，所以写成了变量
    msg_send = u'你的朋友'+warning_name+'可能正处于危险'
    ret = True
    try:
        msg = MIMEText(msg_send, 'plain', 'utf-8')
        msg['From'] = formataddr([u"警告员", email_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = u"警告"  # 邮件的主题，也可以说是标题
        email_server.sendmail(email_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    except Exception as e:  # 如果try中的语句没有执行，则会执行下面的ret=False
        ret = False
        traceback.print_exc()
    return ret


