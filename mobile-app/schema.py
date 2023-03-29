#!/usr/bin/env python

#-----------------------------------------------------------------------
# schema.py
# Authors: Aidan Phillips
#-----------------------------------------------------------------------

import sqlalchemy
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()
#-----------------------------------------------------------------------

class Organization(Base):
    __tablename__ = 'organizations'
    org_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    org_name = sqlalchemy.Column(sqlalchemy.String)
    phone = sqlalchemy.Column(sqlalchemy.String)
    website = sqlalchemy.Column(sqlalchemy.String)
    photo_url = sqlalchemy.Column(sqlalchemy.String)
    street = sqlalchemy.Column(sqlalchemy.String)
    zip_code = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('zip_codes.zip_code'))
    services = sqlalchemy.Column(sqlalchemy.String)
    ownerships = sqlalchemy.orm.relationship("Ownership", back_populates="organization")

class Offering(Base):
    __tablename__ = 'offerings'
    off_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    days_open = sqlalchemy.Column(sqlalchemy.String)
    days_desc = sqlalchemy.Column(sqlalchemy.String)
    start_time = sqlalchemy.Column(sqlalchemy.String)
    end_time = sqlalchemy.Column(sqlalchemy.String)
    init_date = sqlalchemy.Column(sqlalchemy.String)
    close_date = sqlalchemy.Column(sqlalchemy.String)
    off_service = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('services.service_id'))
    group_served = sqlalchemy.Column(sqlalchemy.Integer)
    off_desc = sqlalchemy.Column(sqlalchemy.String)
    ownerships = sqlalchemy.orm.relationship("Ownership", back_populates="offering")

class ZipCode(Base):
    __tablename__ = 'zip_codes'
    zip_code = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    city = sqlalchemy.Column(sqlalchemy.String)
    state = sqlalchemy.Column(sqlalchemy.String)

class Service(Base):
    __tablename__ = 'services'
    service_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    service_name = sqlalchemy.Column(sqlalchemy.String)

class Ownership(Base):
    __tablename__ = 'org_ownership'
    org_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('organizations.org_id'), primary_key=True)
    off_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('offerings.off_id'), primary_key=True)
    organization = sqlalchemy.orm.relationship("Organization", back_populates="ownerships")
    offering = sqlalchemy.orm.relationship("Offering", back_populates="ownerships")
