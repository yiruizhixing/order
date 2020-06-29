# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from common.models.bm.BmExam import BmExam
from common.models.people.People import People
from application import db




class BmInfo(db.Model):
    __tablename__ = 'bm_info'

    id = db.Column(db.Integer, primary_key=True)
    bm_exam_id = db.Column(db.ForeignKey('bm_exam.id', onupdate='CASCADE'), nullable=False, unique=True)
    people_id = db.Column(db.ForeignKey('people.id', onupdate='CASCADE'), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    xunkao_id = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    kaodian_id = db.Column(db.Integer, nullable=False)
    kaodian_name = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    kemu = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    xk_date = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    sh_status = db.Column(db.Integer, nullable=False)
    sh_admin = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    sh_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    _from = db.Column('from', db.String(200), nullable=False, server_default=db.FetchedValue())
    beizhu1 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    beizhu2 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    beizhu3 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    bm_exam = db.relationship('BmExam', primaryjoin='BmInfo.bm_exam_id == BmExam.id', backref='bm_infos')
    people = db.relationship('People', primaryjoin='BmInfo.people_id == People.id', backref='bm_infos')


