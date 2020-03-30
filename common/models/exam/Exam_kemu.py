# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from common.models.exam.Exam import DicDesc
from common.models.exam.Exam import DicStatu
from common.models.exam.Exam import Exam
from application import db




class ExamKemu(db.Model):
    __tablename__ = 'exam_kemu'

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.ForeignKey('exam_list.id', onupdate='CASCADE'), nullable=False, index=True)
    exam_name = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    changci = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    kemu_name = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    start_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    last_time = db.Column(db.Integer, nullable=False)
    kaochang = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    beizhu1 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    beizhu2 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    exam = db.relationship('Exam', primaryjoin='ExamKemu.exam_id == Exam.id', backref='exam_kemus')



