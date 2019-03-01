# -*- coding: utf-8 -*-
import json

from . import db


class User(db.Model):
    # 给表重新定义一个名称，默认名称是类名的小写，比如该类默认的表名是user。
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(16))
    email_address = db.Column(db.String(40))
    # 给User类创建一个picture属性，关联pitures表。
    # backref是反向的给Picture类创建一个user属性，关联users表。这是flask特殊的属性。
    pictures = db.relationship('Picture', backref="user")

    def __init__(self, name, password, email_address):
        self.name = name
        self.password = password
        self.email_address = email_address

    def __repr__(self):
        user_dict = {'id': self.id, 'name': self.name, 'password': self.password, 'email_address': self.email_address}
        user_json = json.dumps(user_dict)
        return user_json


class Picture(db.Model):
    # 给表重新定义一个名称，默认名称是类名的小写，比如该类默认的表名是user。
    __tablename__ = "pictures"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    adress = db.Column(db.String(255), unique=True)
    # 创建一个外键，和django不一样。flask需要指定具体的字段创建外键，不能根据类名创建外键
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, name, adress, user_id):
        self.name = name
        self.adress = adress
        self.user_id = user_id

    def __repr__(self):
        picture_dic = {'id': self.id, 'name': self.name, 'adress': self.adress, 'user_id': self.user_id}
        picture_json = json.dumps(picture_dic)
        return picture_json
