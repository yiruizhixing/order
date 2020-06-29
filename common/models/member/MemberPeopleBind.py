# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from common.models.member.Member import Member
from common.models.people.People import People
from application import db


class MemberPeopleBind(db.Model):
    __tablename__ = 'member_people_bind'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.ForeignKey('member.id', onupdate='CASCADE'), nullable=False, unique=True)
    people_id = db.Column(db.ForeignKey('people.id', onupdate='CASCADE'), nullable=False, unique=True)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    beizhu1 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    beizhu2 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    beizhu3 = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    member = db.relationship('Member', primaryjoin='MemberPeopleBind.member_id == Member.id', backref='member_people_binds')
    people = db.relationship('People', primaryjoin='MemberPeopleBind.people_id == People.id', backref='member_people_binds')


