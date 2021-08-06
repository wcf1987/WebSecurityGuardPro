# coding:utf-8
from random import randint
from models.account.account_user_model import User
from datetime import datetime
from libs.yun_tong_xun.yun_tong_xun_lib import sendTemplateSMS
from libs.flash.flash_lib import flash


def create_captcha_img(self, pre_code, code):
    """生成验证码，保存到redis"""
    if pre_code:
        self.conn.delete("captcha:%s" % pre_code)  #删除上一次redis缓存   存在bug  两个人同时点
    text, img = create_captcha()
    self.conn.setex("captcha:%s" % code, text.lower(), 60)  #存到redis 超过60秒消除
    return img




def login(self, name, password):
    """02登录函数"""
    print name, password
    if name == '' and password == '':
        return {'status': False, 'msg': '输入用户名或密码'}
    user = User.by_name(name)
    if user and user.auth_password(password):
        user.last_login = datetime.now()  # 最后一次登录时间
        user.loginnum += 1  # 登录次数加1
        self.db.add(user)
        self.db.commit()  # 提交
        self.session.set('user_name', user.name)  # 将用户名存入缓存
        return {'status': True, 'msg': '登录成功'}
    return {'status': False, 'msg': '用户名输入错误或者密码不正确'}





def regist(self, name, mobile, mobile_captcha, password1, password2, captcha, code):
    """04注册函数
    判断类型  边界值
    """
    if self.conn.get("captcha:%s" % code) != captcha.lower():
        flash(self, '图片验证码不正确', 'error')
        return {'status': False, 'msg': '图片验证码不正确'}
    if self.conn.get("mobile_code:%s" % mobile) != mobile_captcha:
        flash(self, '短信验证码不正确', 'error')
        return {'status': False, 'msg': '短信验证码不正确'}
    if password1 != password2:
        flash(self, '两次密码不一致', 'error')
        return {'status': False, 'msg': '两次密码不一致'}
    #存入数据库
    user = User.by_name(name)
    if user is not None:
        flash(self, '用户名已存在', 'error')
        return {'status': False, 'msg': '用户名已存在'}
    user = User()
    user.name = name
    user.password = password2
    user.mobile = mobile
    self.db.add(user)
    self.db.commit()
    flash(self, '注册成功', 'success')
    return {'status': True, 'msg': '注册成功'}



