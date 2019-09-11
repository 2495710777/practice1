import os
import datetime

import tornado.ioloop, tornado.web
from tornado.options import parse_command_line, define, options
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base


define("host", default='localhost', help="主机地址",type=str)
define("port", default='9090', help="主机端口",type=int)

# 建⽴连接与数据库的连接
engine = create_engine('mysql+pymysql://lwq:123123@localhost:3306/tornado')
Base = declarative_base(bind=engine)  # 创建模型的基础类
Session = sessionmaker(bind=engine)  # 这两个都是类，绑定engine创建会话类
session = Session()


class User(Base):
    # 类本身对应数据库里的表结构
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True)
    birthday = Column(Date, default=datetime.date(1990, 1, 1))
    city = Column(String(10), default='上海')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument('id', '0')
        q = session.query(User)
        users = q.filter(User.id >= 1)

        if id == '0':
            foo = []
            q = session.query(User)
            user = q.filter(User.id > 0)
            for i in user:
                foo.append([i.id, i.name, i.birthday, i.city])
        else:
            q = session.query(User)
            user = q.filter(User.id == id).first()
            foo = [user.id, user.name, user.birthday, user.city]
        result = []
        for i in users:
            result.append(i.name)
        print(result)
        self.render('user.html', content=result, aaaa=foo)


class GetHandler(tornado.web.RequestHandler):
    def get(self):
        uid = self.get_argument('num', '1')
        q = session.query(User)
        user = q.filter(User.id == uid).first()

        self.render('info.html', content=user)


class ModHandler(tornado.web.RequestHandler):

    def get(self):
        uid = self.get_argument("id", "1")
        q = session.query(User)
        user=q.get(uid)
        self.render('post.html', content=user)

    def post(self):
        uid = self.get_argument("uid")
        name = self.get_argument("name")
        city = self.get_argument("city")
        q = session.query(User)
        user = q.filter(User.id == uid).first()
        print(user.id, user.name)
        user.name = name
        user.city = city
        session.commit()

        self.render("info.html", content=user)


class StaticTestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('static_test.html')


def make_app():
    routes = [
        (r'/', MainHandler),
        (r'/get', GetHandler),
        (r'/mod', ModHandler),
        (r'/static', StaticTestHandler)

    ]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'statics')
    print(base_dir)
    return tornado.web.Application(routes,
                                   template_path=template_dir,
                                   static_path=static_dir,
                                   debug=True)


if __name__ == '__main__':
    parse_command_line()
    app = make_app()
    app.listen(options.port, options.host)
    tornado.ioloop.IOLoop.current().start()
