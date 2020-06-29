# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db


class BmExam(db.Model):
    __tablename__ = 'bm_exam'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    exam_id = db.Column(db.Integer, nullable=False)
    exam_name = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    show_exam_name = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    numbers = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    x_rules = db.Column(db.String(1000), nullable=False, server_default=db.FetchedValue())
    m_rules = db.Column(db.String(1000), nullable=False, server_default=db.FetchedValue())
    rule_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    start_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    end_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    beizhu = db.Column(db.String(2000), nullable=False, server_default=db.FetchedValue())
    beizhu2 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    beizhu3 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
