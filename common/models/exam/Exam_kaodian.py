# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from common.models.exam.Exam import Exam
from common.models.exam.Kaodian import Kaodian
from application import db


class ExamKaodian(db.Model):
    __tablename__ = 'exam_kaodian'

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.ForeignKey('exam_list.id', onupdate='CASCADE'), nullable=False, index=True)
    exam_name = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    kaodian_id = db.Column(db.ForeignKey('kaodian.id', onupdate='CASCADE'), nullable=False, index=True)
    kaodian_name = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    kaodian_address = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    kaochang = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    kaochang_stnum = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    kemu = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    xunkao_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    menjian_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    beizhu1 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    beizhu2 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    beizhu3 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    exam = db.relationship('Exam', primaryjoin='ExamKaodian.exam_id == Exam.id', backref='exam_kaodians')
    kaodian = db.relationship('Kaodian', primaryjoin='ExamKaodian.kaodian_id == Kaodian.id', backref='exam_kaodians')


