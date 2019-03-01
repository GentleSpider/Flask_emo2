import os
from os import path

from flask import request, render_template

from . import auth
from ..model import *
from ..pictures import picture_basedir

USER_ID = None


# PICTURE_SAVE_DIR = None


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    elif request.method == 'GET':
        username = request.args['username']
        password = request.args['password']
    else:
        res_dic = {'res': 'login_failed', 'log_stat': 'error', 'function': 'login'}
        res_json = json.dumps(res_dic)
        return res_json

    res = db.session.query(User).filter_by(name=username, password=password).first()
    if res != None:
        global USER_ID
        USER_ID = res.id
        res_dic = {'res': 'login success', 'log_stat': 'ok', 'function': 'login'}
        res_json = json.dumps(res_dic)
        # return render_template('result.html',title='login result' ,message=res)
        return res_json
    else:
        res_dic = {'res': 'do not login or username password error'}
        res_json = json.dumps(res_dic)
        return res_json
        # return u"未注册或者用户名密码错误"


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    global USER_ID
    USER_ID = None
    # return render_template('result.html', title="logout result", message='logout successfully')
    res_dic = {'res': 'logout success', 'log_stat': 'error'}
    res_json = json.dumps(res_dic)
    return res_json
    # test
    # if username == 'liuzhu':
    #     return "username:%s\npassword:%s" % (username, password)
    # else:
    #     return u"未注册或者用户名密码错误"


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        username = request.args['username']
        password = request.args['password']
        email_address = request.args['email_address']

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email_address = request.form['email_address']
    else:
        res_dic = {'res': 'method error'}
        res_json = json.dumps(res_dic)
        return res_json

    res = db.session.query(User).filter_by(name=username).first()
    if res is not None:
        res_json = json.dumps({'res': 'register exist'})
        return res_json

    try:
        new_user = User(name=username, password=password, email_address=email_address)
        db.session.add(new_user)
        db.session.commit()
    except IOError:
        print(u'注册异常')
        res_json = json.dumps({'res': 'register failed'})
        return res_json

    res_dic = {'res': 'register success', 'function': 'register'}
    res_json = json.dumps(res_dic)
    return res_json
    # return render_template('result.html' , title='register result' ,message='register ok')


@auth.route('/user_del', methods=['POST'])
def user_del():
    if request.method == 'POST':
        user_name = request.form['user_name']
    else:
        res_json = json.dumps({'res': 'method erros', 'function': 'user_del'})
        return res_json

    import traceback
    try:
        del_user = Picture.query.fliter_by(name=user_name).first()
        db.session.delete(del_user)
        db.session.commit()
    except Exception as e:
        traceback.print_exc();
    return json.dumps({'res': 'user_del success', 'function': 'user_del'})


@auth.route('/picture_add', methods=['POST'])
def picture_add():
    picture_name = request.form['picture_name']
    picture_file = request.form['picture_file']
    global USER_ID
    if USER_ID is None:
        res_dic = {'res': 'do not login', 'function': 'picture_add'}
        res_json = json.dumps(res_dic)
        return res_json
        # return 'do not login in picture add'
    else:

        picture_user_id = USER_ID
        picture_address = path.join(picture_basedir, str(USER_ID))
        if os.path.exists(picture_address):
            pass
        else:
            os.makedirs(picture_address)

        picture_address = path.join(picture_address, str(picture_name) + '.jpg')

        # global PICTURE_SAVE_DIR
        # PICTURE_SAVE_DIR = picture_address

        import base64
        picture_file = base64.b64decode(picture_file)
        fout = open(picture_address, 'wb')
        fout.write(picture_file)
        fout.close()
        # picture_file.save(picture_address)

    try:
        new_picture = Picture(name=picture_name, adress=picture_address, user_id=picture_user_id)
        db.session.add(new_picture)
        db.session.commit()
    except IOError as e:
        print(e)

    res_dic = {'res': 'picture add success', 'function': 'picture add'}
    res_json = json.dumps(res_dic)
    return res_json
    # return render_template('result.html', message='picture add successfully', add_info=str(picture_address))


# @auth.route('/picture_file_add', methods=['POST'])
# def picture_file_add():
#     global PICTURE_SAVE_DIR
#     if PICTURE_SAVE_DIR != None:
#         picture_file = request.files['picture_file']
#         picture_file.save(PICTURE_SAVE_DIR)
#         picture_add_info = PICTURE_SAVE_DIR
#         PICTURE_SAVE_DIR = None
#         return render_template('result.html', message='picture file add succussfully', add_info=picture_add_info)
#     else:
#         return 'picture information not compeletely in picture file adding'


@auth.route('/picture_del', methods=['POST', 'GET'])
def picture_del():
    if request.method == 'POST':
        picture_name = request.form['picture_name']
    elif request.method == 'GET':
        picture_name = request.args['picture_name']
    else:
        res_dic = {'res': 'picture del failed', 'function': 'picture_del'}
        res_json = json.dumps(res_dic)
        return res_json

    if USER_ID is None:
        res_json = json.dumps({'res': 'do not login', 'function': 'picture del'})
        return res_json
        # return 'do not login in picture delete'
    else:
        pass
        # picture_name = request.form['picture_name']
    try:
        del_picture = Picture.query.fliter_by(name=picture_name).first()
        db.session.delete(del_picture)
        db.session.commit()
    except IOError as e:
        print(e)
    res_json = json.dumps({'res': 'picture del success', 'function': 'picture del'})
    return res_json
    # return render_template("result.html",message="picture delete successfully")


@auth.route('/picture_check', methods=['POST'])
def picture_check():
    # '''
    #     # 检测图片，返回人脸对比度和情绪
    #     # :return:
    #     # '''
    picture_check_file = request.form['picture_check_file']
    if USER_ID is None:
        res_json = json.dumps({'res': 'do not login', 'function': 'picture_check'})
        return res_json
        # return render_template('result.html', message='do not login in picture_check')
    else:
        # # test
        # import base64
        # picture_check_file = request.form['picture_check_file']
        # picture_file = base64.b64decode(picture_check_file)
        # fout = open(path.join(picture_basedir, '2.jpg'), 'wb')
        # fout.write(picture_file)
        # fout.close()
        # return "hello"

        from app.face_api import baidu_client
        import base64
        # picture_check_file = request.form['picture_check_file']
        picture_check_dir = path.join(picture_basedir, str(USER_ID))
        for fpaths, dirnames, filenames in os.walk(picture_check_dir):
            for filename in filenames:
                filepath = path.join(fpaths, filename)
                if filepath.endswith('.jpg') or filepath.endswith('JPG'):
                    result = baidu_client.match([
                        {
                            'image': str(base64.b64encode(open(filepath, 'rb').read()), encoding='utf-8'),
                            'image_type': 'BASE64',
                        },
                        {
                            'image': picture_check_file,
                            'image_type': 'BASE64',
                        }
                    ])
                    from app.face_api import ext_api
                    if result['result']['score'] > 60:
                        res_name = filename.split('.')
                        res_name = res_name[0]
                        res_emo = ext_api.baidu_emo_api(picture_check_file, 'BASE64')
                        res_dic = {'res': 'picture_check_success', 'return_stat': 'picture_check_ok',
                                   'return_name': res_name, 'score': result['result']['score'], 'emotion': res_emo,
                                   'function': 'picture_check', 'email_flag': 'false'}
                        if res_emo in ['fear', 'angry' , 'sadness']:
                            res = db.session.query(User).filter_by(id=USER_ID).first()
                            reciver_email = res.email_address
                            warn_name = res_name
                            ext_api.py3_warn_mail(reciver_email, warn_name)
                            res_dic['email_flag'] = 'true'
                        res_json = json.dumps(res_dic)
                        return res_json

            res_json = json.dumps({'res': 'picture_check_failed'})
            return res_json


@auth.route('/baidu_test', methods=['GET', 'POST'])
def baidu_test():
    import base64
    from . import baidu_client
    import os
    filepath = os.path.abspath(os.path.dirname(__file__))
    result = baidu_client.match([
        {
            'image': str(base64.b64encode(open(os.path.join(filepath, '1.jpg'), 'rb').read()), encoding='utf-8'),
            'image_type': 'BASE64',
        },
        {
            'image': str(base64.b64encode(open(os.path.join(filepath, '2.jpg'), 'rb').read()), encoding='utf-8'),
            'image_type': 'BASE64',
        }
    ])
    return render_template('result.html', message=result)


@auth.route('/picture_upload_test', methods=['POST'])
def picture_upload_test():
    '''
    测试上传文件
    :return:
    '''
    from os import path
    picture_file = request.files['picture_file']
    # return render_template('result.html', message = 'hello')
    picture_address = path.join(picture_basedir, '1.jpg')
    # return render_template('result.html', message = picture_address)
    picture_file.save(picture_address)
    return render_template('result.html', message='picture_upload_test successfully')


@auth.route('/')
def welcome():
    # res = db.session.query(User).filter_by(name='liuzhu').first()
    # res_key = res.password
    # return res_key
    return "welcome"
