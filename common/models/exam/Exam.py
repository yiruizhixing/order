# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from application import db


class DicDesc(db.Model):
    __tablename__ = 'dic_desc'

    dic_id = db.Column(db.Integer, primary_key=True)
    dic_name = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class DicStatu(db.Model):
    __tablename__ = 'dic_status'

    status_id = db.Column(db.Integer, primary_key=True)
    dic_id = db.Column(db.ForeignKey('dic_desc.dic_id', onupdate='CASCADE'), nullable=False, index=True)
    status_name = db.Column(db.String(200), nullable=False)
    dic_name = db.Column(db.String(200))
    beizhu = db.Column(db.String(200))
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    dic = db.relationship('DicDesc', primaryjoin='DicStatu.dic_id == DicDesc.dic_id', backref='dic_status')





class Exam(db.Model):
    __tablename__ = 'exam_list'

    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    exam_code = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    abbreviation = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    exam_date = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    summary = db.Column(db.String(300), nullable=False, server_default=db.FetchedValue())
    exam_status = db.Column(db.ForeignKey('dic_status.status_id', onupdate='CASCADE'), nullable=False, index=True)
    exam_cat = db.Column(db.ForeignKey('dic_status.status_id', onupdate='CASCADE'), nullable=False, index=True)
    keshu = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    canbu = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    days = db.Column(db.Float, nullable=False, server_default=db.FetchedValue())
    kaodian = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    # 关系属性和反向引用
    dic_statu = db.relationship('DicStatu', primaryjoin='Exam.exam_cat == DicStatu.status_id', backref='dicstatu_exams')
    dic_statu1 = db.relationship('DicStatu', primaryjoin='Exam.exam_status == DicStatu.status_id', backref='dicstatu_exams_0')
