#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Authors: Aidan Phillips, Yousef Amin
#-----------------------------------------------------------------------

import contextlib
import sys
import csv
import psycopg2
from decouple import config
import sqlalchemy
from sqlalchemy import text
import offering as offmod
import organization as orgmod
import init
from schema import Offering, Organization
from schema import Ownership, Service, PeopleGroup

engine = init.engine

#-----------------------------------------------------------------------
# find_offerings()
# Makes a list of offering objects based on the filter
# Parameters: sort - a string containing the column to sort by
#             filter - a tuple with one string for each column we want
#                      to filter by
# Returns: a list of offering objects
#-----------------------------------------------------------------------
def find_offerings(filter):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Organization.org_name,
                Offering.title, Offering.days_open,
                Offering.start_time, Offering.end_time,
                Offering.init_date, Offering.close_date,
                Service.service_type, PeopleGroup.people_group,
                Offering.off_desc) \
                .select_from(Organization) \
                .join(Ownership) \
                .join(Offering) \
                .join(Service) \
                .join(PeopleGroup) \
                .filter(Organization.org_name.ilike(filter))
            
            results = query.all()
            offerings = []
            for row in results:
                offerings.append(offmod.Offering(row))
            return offerings
        
    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

#-----------------------------------------------------------------------
# find_offerings()
#-----------------------------------------------------------------------
def find_organizations():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Organization.org_name,
                Organization.phone, Organization.website,
                Organization.street, Organization.zip_code)
            results = query.all()

            organizations = []
            if results is not None:
                for row in results:
                    organizations.append(orgmod.Organization(row))
            return organizations

    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

#-----------------------------------------------------------------------
# bulk_update()
# Reads a CSV file and updates the database with the information
# Parameters: filename - a string containing the name of the file to
#                        read from
# Returns: 0 if successful, 1 if not
#-----------------------------------------------------------------------
def bulk_update(filename):
    # Truncate tables so we can insert new data
    # comment out for testing
    # exe_stmt('TRUNCATE offerings RESTART IDENTITY CASCADE', ())
    # exe_stmt('TRUNCATE org_ownership RESTART IDENTITY CASCADE', ())
    # exe_stmt('TRUNCATE organizations RESTART IDENTITY CASCADE', ())
    try:
        with sqlalchemy.orm.Session(engine) as session:
            session.execute(text('TRUNCATE offerings RESTART '
                'IDENTITY CASCADE'))
            session.execute(text('TRUNCATE org_ownership RESTART '
                'IDENTITY CASCADE'))
            session.execute(text('TRUNCATE organizations RESTART '
                'IDENTITY CASCADE'))
            session.execute(text('TRUNCATE services RESTART '
                'IDENTITY CASCADE'))
            session.execute(text('TRUNCATE people_groups RESTART '
                'IDENTITY CASCADE'))
            
            with open(filename, 'r', encoding='utf-8') as csv_file:
                csv_reader = list(csv.DictReader(csv_file))
                organizations = 0
                offerings = 0
                services = 0
                groups = 0
                # TODO: organization counter for efficiency
                for row in csv_reader:
                    # query org_id based on name, if not there then
                    # add it
                    query = session.query(Organization.org_id) \
                        .filter(Organization.org_name.ilike(
                        row.get('Organization Name')))
                    res = query.first()
                    # if organization not in database, add it, else
                    # save the org_id
                    if not res:
                        organizations += 1
                        insert_stmt = text('INSERT INTO organizations '
                            '(org_name, phone, website, street, '
                            'zip_code) VALUES (:org_name, :phone, '
                            ':website, :street, :zip_code)')
                        session.execute(insert_stmt, {
                            'org_name': row.get('Organization Name'),
                            'phone': row.get('Phone Number'),
                            'website': row.get('Website'),
                            'street': row.get('Street'),
                            'zip_code': row.get('Zip Code')
                        })
                        org_id = organizations
                    else:
                        org_id = res[0]

                    # get service and group ids from database
                    query = session.query(Service.service_id) \
                        .filter(Service.service_type.ilike(
                        row.get('Service')))
                    res = query.first()
                    # if service not in database, add it
                    if not res:
                        services += 1
                        insert_stmt = text('INSERT INTO services '
                            '(service_type) VALUES (:service_type)')
                        session.execute(insert_stmt, {
                            'service_type': row.get('Service')
                        })
                        # get the service_id of the service we just
                        # added
                        query = session.query(Service.service_id) \
                            .filter(Service.service_type.ilike(
                            row.get('Service')))
                        service_id = services
                    else:
                        service_id = res[0]
                    
                    # repeat for group
                    query = session.query(PeopleGroup.group_id) \
                        .filter(PeopleGroup.people_group.ilike(
                        row.get('People Served')))
                    if not res:
                        groups += 1
                        insert_stmt = text('INSERT INTO people_groups '
                            '(people_group) VALUES (:people_group)')
                        session.execute(insert_stmt, {
                            'people_group': row.get('People Served')
                        })
                        query = session.query(PeopleGroup.group_id) \
                            .filter(PeopleGroup.people_group.ilike(
                            row.get('People Served')))
                        group_id = groups
                    else:
                        group_id = res[0]
                    
                    # add offering to database
                    ins_off_stmt = text('INSERT INTO offerings '
                        '(title, days_open, days_desc, start_time, '
                        'end_time, init_date, close_date, off_service, '
                        'group_served, off_desc) VALUES '
                        '(:title, :days_open, :days_desc, :start_time, '
                        ':end_time, :init_date, :close_date, '
                        ':off_service, :group_served, :off_desc)')
                    # if no offering title, use organization name
                    if row.get('Title') == '':
                        row['Title'] = row.get('Organization Name')
                    # replace empty cells with None
                    for key in row:
                        if row[key] == '':
                            row[key] = None
                    session.execute(ins_off_stmt, {
                        'title': row.get('Title'),
                        'days_open': row.get('Days'),
                        'days_desc': row.get('Day Description'),
                        'start_time': row.get('Start Time'),
                        'end_time': row.get('End Time'),
                        'init_date': row.get('Start Date'),
                        'close_date': row.get('End Date'),
                        'off_service': service_id,
                        'group_served': group_id,
                        'off_desc': row.get('Description')
                    })
                    offerings += 1

                    # add organization ownership to database
                    own_ins_stmt = text('INSERT INTO org_ownership '
                        '(org_id, off_id) VALUES (:org_id, :off_id)')
                    session.execute(own_ins_stmt, {
                        'org_id': org_id,
                        'off_id': offerings
                    })
            session.commit()
    except Exception as ex:
        print(ex, file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    print('testing database.py')
    bulk_update('input-sample.csv')
