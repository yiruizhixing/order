# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db, app


class People(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    cat_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    sfzh = db.Column(db.String(18), nullable=False, server_default=db.FetchedValue())
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    xunkao_id = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    weight = db.Column(db.String(4), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    danwei = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    bumen = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    chepai = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    avatar = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    address = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue())
    bankaddr = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue())
    bankcard = db.Column(db.String(19), nullable=False, server_default=db.FetchedValue())
    salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    reg_ip = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    @property
    def status_desc(self):
        return app.config['STATUS_MAPPING'][str(self.status)]

    # 性别虚拟字段
    @property
    def sex_desc(self):
        sex_mapping = {
            "0": "未知",
            "1": "男",
            "2": "女"
        }
        return sex_mapping[str(self.sex)]
