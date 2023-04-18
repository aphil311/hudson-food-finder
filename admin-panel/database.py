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
import offering as offmod
import organization as orgmod
import init
from schema import Offering, Organization, Ownership, Service, PeopleGroup

engine = init.engine

_DATABASE_URL_ = config('DB_URL')

#-----------------------------------------------------------------------
# query()
# Opens a connection to the database and executes a SQL query
# Parameters: stmt_str - a string containing a SQL statement
#             args - a list containing the arguments to use with the
#                    SQL statement
# Returns: results of the query as a table
#-----------------------------------------------------------------------
def query(stmt_str, args):
    try:
        with psycopg2.connect(_DATABASE_URL_) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute(stmt_str, args)
                table = cursor.fetchall()
                return table
    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

#-----------------------------------------------------------------------
# exe_stmt()
# Opens a connection to the database and executes a SQL statement
# Parameters: stmt_str - a string containing a SQL statement
#             args - a list containing the arguments to use with the
#                    SQL statement
# Returns: none
#-----------------------------------------------------------------------
def exe_stmt(stmt_str, args):
    try:
        with psycopg2.connect(_DATABASE_URL_) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute(stmt_str, args)
    except Exception as ex:
        print(ex, file=sys.stderr)

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
    ORG_CUTOFF = 5
    SERVICE_CUTOFF = 12
    GROUP_CUTOFF = 13
    # Truncate tables so we can insert new data
    # comment out for testing
    exe_stmt('TRUNCATE offerings RESTART IDENTITY CASCADE', ())
    exe_stmt('TRUNCATE org_ownership RESTART IDENTITY CASCADE', ())
    exe_stmt('TRUNCATE organizations RESTART IDENTITY CASCADE', ())
    try:
        with open(filename, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # skip header row
                if line_count != 0:
                    sel_orgid_inputs = []
                    sel_orgid = 'SELECT org_id FROM organizations '
                    sel_orgid += 'WHERE org_name = %s'
                    for cell in row[:1]:
                        sel_orgid_inputs.append(cell)
                    res = query(sel_orgid, sel_orgid_inputs)
                    # if organization not in database, add it, else
                    # save the org_id
                    if not res:
                        ins_org = 'INSERT INTO organizations '
                        ins_org += '(org_name, phone, website, street, '
                        ins_org += 'zip_code) VALUES (%s, %s, %s, %s, '
                        ins_org += '%s)'
                        ins_org_inputs = []
                        org_name = row[0]
                        ins_org_inputs.append(org_name)
                        print(org_name)
                        for cell in row[1:ORG_CUTOFF]:
                            ins_org_inputs.append(cell)
                        exe_stmt(ins_org, ins_org_inputs)
                        res = query(sel_orgid, sel_orgid_inputs)
                    org_id = res[0][0]

                    # get service and group ids from database
                    sel_serviceid_inputs = []
                    sel_serviceid_inputs.append(row[SERVICE_CUTOFF])
                    sel_serviceid = 'SELECT service_id FROM services '
                    sel_serviceid += 'WHERE service_type = %s'
                    service_id = query(sel_serviceid,
                        sel_serviceid_inputs)
                    # if service not in database, add it
                    if not service_id:
                        ins_service = 'INSERT INTO services '
                        ins_service += '(service_type) VALUES (%s)'
                        exe_stmt(ins_service, sel_serviceid_inputs)
                        service_id = query(sel_serviceid,
                            sel_serviceid_inputs)

                    service_id = service_id[0][0]
                    
                    # repeat for group
                    sel_groupid_inputs = []
                    sel_groupid_inputs.append(row[GROUP_CUTOFF])
                    sel_groupid = 'SELECT group_id FROM people_groups '
                    sel_groupid += 'WHERE people_group = %s'
                    group_id = query(sel_groupid, sel_groupid_inputs)
                    # if group not in database, add it
                    if not group_id:
                        ins_group = 'INSERT INTO people_groups '
                        ins_group += '(people_group) VALUES (%s)'
                        exe_stmt(ins_group, sel_groupid_inputs)
                        group_id = query(sel_groupid,
                            sel_groupid_inputs)
                    
                    group_id = group_id[0][0]
                    
                    # add offering to database
                    ins_off = 'INSERT INTO offerings '
                    ins_off += '(title, days_open, days_desc, '
                    ins_off += 'start_time, end_time, init_date, '
                    ins_off += 'close_date, off_service, '
                    ins_off += 'group_served, off_desc)'
                    ins_off += 'VALUES (%s, %s, %s, %s, %s, %s, %s, '
                    ins_off += '%s, %s, %s)'
                    ins_off_inputs = []
                    # if no offering title, use organization name
                    if row[ORG_CUTOFF] == '':
                        row[ORG_CUTOFF] = org_name
                    for cell in row[ORG_CUTOFF:SERVICE_CUTOFF]:
                        if cell == '':
                            cell = None
                        ins_off_inputs.append(cell)
                    ins_off_inputs.append(service_id)
                    ins_off_inputs.append(group_id)
                    for cell in row[GROUP_CUTOFF+1:]:
                        if cell == '':
                            cell = None
                        ins_off_inputs.append(cell)
                    exe_stmt(ins_off, ins_off_inputs)

                    # match offering to organization
                    ins_own = 'INSERT INTO org_ownership '
                    ins_own += '(org_id, off_id) VALUES (%s, %s)'
                    ins_own_inputs = []
                    ins_own_inputs.append(org_id)
                    ins_own_inputs.append(line_count)
                    exe_stmt(ins_own, ins_own_inputs)
                # go to next line in csv
                line_count += 1
    except Exception as ex:
        print(ex, file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    print('testing database.py')
    bulk_update('input-sample.csv')
