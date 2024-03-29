#!/usr/bin/env python

#-----------------------------------------------------------------------
# schema.py
# Authors: Aidan Phillips
# Defines the database schema for sqlalchemy
#-----------------------------------------------------------------------

import sqlalchemy
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# Organization
# Represents an organization in the database
#-----------------------------------------------------------------------
class Organization(Base):
    __tablename__ = 'organizations'
    org_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    org_name = sqlalchemy.Column(sqlalchemy.String)
    phone = sqlalchemy.Column(sqlalchemy.String)
    website = sqlalchemy.Column(sqlalchemy.String)
    photo_url = sqlalchemy.Column(sqlalchemy.String)
    street = sqlalchemy.Column(sqlalchemy.String)
    zip_code = sqlalchemy.Column(sqlalchemy.String,
        sqlalchemy.ForeignKey('zip_codes.zip_code'))
    services = sqlalchemy.Column(sqlalchemy.String)
    ownerships = sqlalchemy.orm.relationship("Ownership",
        back_populates="organization")

#-----------------------------------------------------------------------
# Offering
# Represents an offering in the database
#-----------------------------------------------------------------------
class Offering(Base):
    __tablename__ = 'offerings'
    off_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    days_open = sqlalchemy.Column(sqlalchemy.String)
    days_desc = sqlalchemy.Column(sqlalchemy.String)
    start_time = sqlalchemy.Column(sqlalchemy.Time)
    end_time = sqlalchemy.Column(sqlalchemy.Time)
    init_date = sqlalchemy.Column(sqlalchemy.String)
    close_date = sqlalchemy.Column(sqlalchemy.String)
    off_service = sqlalchemy.Column(sqlalchemy.Integer,
        sqlalchemy.ForeignKey('services.service_id'))
    group_served = sqlalchemy.Column(sqlalchemy.Integer,
        sqlalchemy.ForeignKey('people_groups.group_id'))
    off_desc = sqlalchemy.Column(sqlalchemy.String)
    ownerships = sqlalchemy.orm.relationship("Ownership",
        back_populates="offering")

#-----------------------------------------------------------------------
# ZipCode
# Represents a zip code in the database
#-----------------------------------------------------------------------
class ZipCode(Base):
    __tablename__ = 'zip_codes'
    zip_code = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    city = sqlalchemy.Column(sqlalchemy.String)
    state = sqlalchemy.Column(sqlalchemy.String)

#-----------------------------------------------------------------------
# Service
# Represents a service in the database
#-----------------------------------------------------------------------
class Service(Base):
    __tablename__ = 'services'
    service_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    service_type = sqlalchemy.Column(sqlalchemy.String)

#-----------------------------------------------------------------------
# Groups
# Represents a group in the database
#-----------------------------------------------------------------------
class Group(Base):
    __tablename__ = 'people_groups'
    group_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    people_group = sqlalchemy.Column(sqlalchemy.String)

#-----------------------------------------------------------------------
# Ownership
# Represents a many-to-many relationship between organizations and
# offerings
#-----------------------------------------------------------------------
class Ownership(Base):
    __tablename__ = 'org_ownership'
    org_id = sqlalchemy.Column(sqlalchemy.Integer,
        sqlalchemy.ForeignKey('organizations.org_id'), primary_key=True)
    off_id = sqlalchemy.Column(sqlalchemy.Integer,
        sqlalchemy.ForeignKey('offerings.off_id'), primary_key=True)
    organization = sqlalchemy.orm.relationship("Organization",
        back_populates="ownerships")
    offering = sqlalchemy.orm.relationship("Offering",
        back_populates="ownerships")
