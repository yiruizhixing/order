# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from application import db
from common.models.exam.Exam import DicDesc
from common.models.exam.Exam import DicStatu
from common.models.exam.Exam import Exam
from common.models.people.People import People



class ExamKaowu(db.Model):
    __tablename__ = 'exam_kaowu'

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.ForeignKey('exam_list.id', onupdate='CASCADE'), nullable=False, index=True)
    name_id = db.Column(db.ForeignKey('people.id', onupdate='CASCADE'), nullable=False, index=True)
    job = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    workplace = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    kaodian = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    kaochang = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    workdays = db.Column(db.Integer, nullable=False)
    canbu = db.Column(db.Integer, nullable=False)
    beizhu1 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    beizhu2 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    beizhu3 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    exam = db.relationship('Exam', primaryjoin='ExamKaowu.exam_id == Exam.id', backref='exam_kaowus')
    name = db.relationship('People', primaryjoin='ExamKaowu.name_id == People.id', backref='exam_kaowus')





