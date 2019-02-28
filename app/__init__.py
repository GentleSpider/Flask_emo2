# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from os import path
from config import config


basedir = path.abspath(path.dirname(__file__))

db = SQLAlchemy()


def create_app(config_name='default'):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:liuzhu0@localhost:3306/first_flask"
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


    return app



# from flask import Flask,request
# from flask_sqlalchemy import SQLAlchemy
#
#
# app = Flask(__name__)
#
# # url的格式为：数据库的协议：//用户名：密码@ip地址：端口号（默认可以不写）/数据库名
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:liuzhu0@localhost:3306/first_flask"
# # 动态追踪数据库的修改. 性能不好. 且未来版本中会移除. 目前只是为了解决控制台的提示才写的
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# # 创建数据库的操作对象
# db = SQLAlchemy(app)
#
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
# @app.route('/dbtest')
# def db_test():
#     # 删除所有的表
#     db.drop_all()
#
#     # 创建表
#     db.create_all()
#
#
#     # 最后插入完数据一定要提交
#     db.session.commit()
#
#
# if __name__ == '__main__':
#
#     app.run(debug=True)

