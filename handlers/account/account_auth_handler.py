# coding:utf-8

"""
文件说明:
    登录页面所有跳转以及方法处理

"""
from handlers.base.base_handler import BaseHandler






class LoginHandler(BaseHandler):
    """登录"""
    def get(self):
        self.render("account/auth_login.html")

    def post(self):
        name = self.get_argument('name', '')
        password = self.get_argument('password', '')
        code = self.get_argument('code', '')
        captcha_code = self.get_argument('captcha', '')
        result = auth_captche(self, captcha_code, code)
        if result['status'] is False:
            return self.write({'status':400, 'msg': result['msg']})
        result = login(self, name, password)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})

        return self.write({'status':400, 'msg': result['msg']})




class RegistHandler(BaseHandler):
    """04注册函数"""
    def get(self):
        self.render("account/auth_regist.html", message="用户注册")

    def post(self):
        mobile = self.get_argument('mobile','')
        mobile_captcha = self.get_argument('mobile_captcha','')
        name = self.get_argument('name','')
        code = self.get_argument('code','')
        password1 = self.get_argument('password1','')
        password2 = self.get_argument('password2','')
        captcha = self.get_argument('captcha','')
        #result = regist(self, name, mobile, mobile_captcha, password1, password2, captcha, code)
        #if result['status'] is True:
        #    # return self.write({'status': 200, 'msg': result['msg']})
        #    self.redirect('/auth/user_login')
        #    # return self.render('auth/user_login', message=result['msg'])
       # else:
        #    self.redirect('/auth/user_regist')


