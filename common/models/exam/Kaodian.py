# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db, app


class Kaodian(db.Model):
    __tablename__ = 'kaodian'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    address = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    kaochang = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    linkman = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    tel = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
