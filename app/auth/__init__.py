from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import view_login

from app.face_api import baidu_client