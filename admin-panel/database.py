#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Authors: Aidan Phillips, Yousef Amin
#-----------------------------------------------------------------------

import sys
import os
import re
import csv
import sqlalchemy
from sqlalchemy import text
import offering as offmod
import organization as orgmod
import config.init as init
from schema import Offering, Organization, AuthorizedUser
from schema import Ownership, Service, PeopleGroup
from config.definitions import ROOT_DIR

#-----------------------------------------------------------------------
engine = init.engine
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# AUTHORIZATION FUNCTIONS
#-----------------------------------------------------------------------

# is_authorized() ------------------------------------------------------
# Checks if a user is authorized to access the admin panel
# Params: username - the username to check
# Return: True if authorized, False if not, None if error
def is_authorized(username):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(AuthorizedUser) \
                .filter(AuthorizedUser.username == username)
            try:
                query.one()
                return True
            except sqlalchemy.exc.NoResultFound:
                return False

    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

# authorize_email() ----------------------------------------------------
# Adds an email to the AuthorizedUser table
# Params: email - the email to add
# Return: True if successful, None if not
def authorize_email(email):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            session.add(AuthorizedUser(username=email))
            session.commit()
            return True

    except Exception as ex:
        print(ex, file=sys.stderr)
        return None
    
# deauthorize_email() --------------------------------------------------
# Removes an email from the AuthorizedUser table
# Params: email - the email to remove
# Return: True if successful, None if not
def deauthorize_email(email):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            session.query(AuthorizedUser) \
                .filter(AuthorizedUser.username==email) \
                .delete()
            session.commit()
            return True

    except Exception as ex:
        print(ex, file=sys.stderr)
        return None
    
# get_emails() ---------------------------------------------------------
# Returns a list of all emails in the AuthorizedUser table
# Returns: a list of emails
def get_emails():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(AuthorizedUser.username)
            results = query.all()
            emails = []
            for row in results:
                emails.append(row[0])
            return emails

    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

#-----------------------------------------------------------------------
# OFFERING FUNCTIONS
#-----------------------------------------------------------------------

# find_offerings() -----------------------------------------------------
# Makes a list of offering objects based on the filter
# Params: filter - a tuple with one string for each column we want
#           to filter by
# Return: a tuple of length 2
#           - the first element is a list of offering
#           - the second element is a list of expired offerings
def find_offerings(filter):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            # form the query for non-expired offerings
            query = session.query(Organization.org_name,
                Offering.title, Offering.days_open,
                Offering.start_time, Offering.end_time,
                Offering.init_date, Offering.close_date,
                Service.service_type, PeopleGroup.people_group,
                Offering.off_desc, Offering.off_id) \
                .select_from(Organization) \
                .join(Ownership) \
                .join(Offering) \
                .join(Service) \
                .join(PeopleGroup) \
                .filter(Organization.org_name.ilike(filter)) \
                .filter(Offering.close_date > sqlalchemy.func.now()) \
                .order_by(Organization.org_name, Offering.title)
            
            # get all and put into list of offering objects
            results = query.all()
            offerings = []
            for row in results:
                offerings.append(offmod.Offering(row))

            # form the query for expired offerings
            query = session.query(Organization.org_name,
                Offering.title, Offering.days_open,
                Offering.start_time, Offering.end_time,
                Offering.init_date, Offering.close_date,
                Service.service_type, PeopleGroup.people_group,
                Offering.off_desc, Offering.off_id) \
                .select_from(Organization) \
                .join(Ownership) \
                .join(Offering) \
                .join(Service) \
                .join(PeopleGroup) \
                .filter(Organization.org_name.ilike(filter)) \
                .filter(Offering.close_date <= sqlalchemy.func.now())
            
            # get all and put into list of offering objects
            results = query.all()
            expired = []
            for row in results:
                expired.append(offmod.Offering(row))

            return offerings, expired
        
    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

# get_offering() -------------------------------------------------------
# Gets an offering object based on the offering id
# Params: off_id - the id of the offering
# Return: an offering object
def get_offering(off_id):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            # form the query for the offering
            query = session.query(Organization.org_name,
                Offering.title, Offering.days_open,
                Offering.start_time, Offering.end_time,
                Offering.init_date, Offering.close_date,
                Service.service_type, PeopleGroup.people_group,
                Offering.off_desc, Offering.off_id) \
                .select_from(Organization) \
                .join(Ownership) \
                .join(Offering) \
                .join(Service) \
                .join(PeopleGroup) \
                .filter(Offering.off_id == off_id)
            
            # get the result of the query
            results = query.all()
            if results is not None:
                # should only be one result
                return offmod.Offering(results[0])
            else:
                return None
    
    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

# update_off() ---------------------------------------------------------
# Updates an offering in the database
# Params: offering_id - id of offering to update
#         inputs - dictionary of inputs from form
# Return: 0 if successful, 1 if error
def update_off(offering_id, inputs):
    try:
        with sqlalchemy.orm.session.Session(engine) as session:
            # update offerings
            offering = session.query(Offering).filter_by(off_id=offering_id).first()
            setattr(offering, 'title', inputs['title'])
            setattr(offering, 'days_open', inputs['days_open'])
            setattr(offering, 'start_time', inputs['start_time'])
            setattr(offering, 'end_time', inputs['end_time'])
            setattr(offering, 'init_date', inputs['start_date'])
            setattr(offering, 'close_date', inputs['end_date'])

            query = session.query(Service.service_id) \
                    .filter(Service.service_type.like(
                    inputs['service']))
            res = query.first()
            if not res:
                # insert new service
                insert_stmt = text('INSERT INTO services '
                    '(service_type) VALUES (:service_type)')
                session.execute(insert_stmt, {
                    'service_type': inputs['service']
                })
                # get the service_id of the service we just
                # added
                service_id = session.query(Service).count()
                setattr(offering, 'off_service', service_id)
            else:
                service_id = res[0]
                setattr(offering, 'off_service', service_id)

            query = session.query(PeopleGroup.group_id) \
                    .filter(PeopleGroup.people_group.like(
                    inputs['group']))
            res = query.first()
            if not res:
                # insert new service
                insert_stmt = text('INSERT INTO people_groups '
                    '(people_group) VALUES (:group)')
                session.execute(insert_stmt, {
                    'group': inputs['group']
                })
                # get the service_id of the service we just
                # added
                group_id = session.query(PeopleGroup).count()
                setattr(offering, 'group_served', group_id)
            else:
                group_id = res[0]
                setattr(offering, 'group_served', group_id)

            setattr(offering, 'off_desc', inputs['description'])
            session.commit()
            return 0
    except Exception as ex:
        print(ex, file=sys.stderr)
        return 1

# find_organizations() -------------------------------------------------
# Gets all organizations from the database
# Return: a list of organization objects
def find_organizations():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Organization.org_name,
                Organization.phone, Organization.website,
                Organization.street, Organization.zip_code,
                Organization.org_id) \
                .order_by(Organization.org_name)
            results = query.all()

            organizations = []
            if results is not None:
                for row in results:
                    organizations.append(orgmod.Organization(row))
            return organizations

    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

# get_organization() ---------------------------------------------------
# Gets an organization object based on the organization id
# Params: org_id - the id of the organization
# Return: an organization object
def get_organization(org_id):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Organization.org_name,
                Organization.phone, Organization.website,
                Organization.street, Organization.zip_code,
                Organization.org_id) \
                .filter(Organization.org_id == org_id) \

            results = query.all()
            if results is not None:
                return orgmod.Organization(results[0])
            else:
                return None
    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

# update_org() ---------------------------------------------------------
# Updates an organization in the database
# Params: organization_id - id of organization to update
#         inputs - dictionary of inputs from form
# Return: 0 if successful, 1 if error
def update_org(organization_id, inputs):
    try:
        with sqlalchemy.orm.session.Session(engine) as session:
            organization = session.query(Organization).filter_by(org_id=organization_id).first()
            setattr(organization, 'org_name', inputs['name'])
            setattr(organization, 'phone', inputs['phone'])
            setattr(organization, 'website', inputs['website'])
            setattr(organization, 'street', inputs['address'])

            session.commit()
            return 0
    except Exception as ex:
        print(ex, file=sys.stderr)
        return 1

#-----------------------------------------------------------------------
# CSV FUNCTIONS
#-----------------------------------------------------------------------

# get_csv() ------------------------------------------------------------
# Gets all organizations from the database and makes a csv file
# Return: 0 if successful, 1 if error
def get_csv():
    try:
        with sqlalchemy.orm.Session(engine) as session:
            # values for each field related to an offering
            query = session.query(Organization.org_name,
                Organization.phone, Organization.website,
                Organization.photo_url,
                Organization.street, Organization.zip_code,
                Offering.title, Offering.days_open,
                Offering.days_desc,
                Offering.start_time, Offering.end_time,
                Offering.init_date, Offering.close_date,
                Service.service_type, PeopleGroup.people_group,
                Offering.off_desc) \
                .select_from(Organization) \
                .join(Ownership) \
                .join(Offering) \
                .join(Service) \
                .join(PeopleGroup)
            results = query.all()

            for row in results:
                print (row)

            # write to csv file
            file_path = os.path.join(ROOT_DIR, 'static',
                'files', 'output.csv')
            with open (file_path, 'w', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Organization', 'Phone Number',
                    'Website', 'Photo URL', 'Street', 'Zip Code', 'Title', 'Days',
                    'Day Description', 'Start Time', 'End Time', 'Start Date',
                    'End Date', 'Service', 'People Served', 'Description'])
                for row in results:
                    csv_writer.writerow(row)
                return 0
                    
    except Exception as ex:
        print(ex, file=sys.stderr)
        return 1

# validate_csv() -------------------------------------------------------
# Validates a csv file
# Params: file - the csv file to validate
# Return: 0 if successful, error message if error
def validate_file(csv_reader):
    # check if file is empty
    if csv_reader is None:
        return 'File is empty'
    # check if file has correct number of columns
    if len(csv_reader[0]) != 16:
        return 'File does not have the 16 required columns'
    # check if file has correct column names
    for key in csv_reader[0].keys():
        if key not in ['Organization', 'Phone Number', 'Website', 
            'Photo URL', 'Street', 'Zip Code', 'Title', 'Days',
            'Day Description', 'Start Time', 'End Time', 'Start Date',
            'End Date', 'Service', 'People Served', 'Description']:
            return 'Column name \"' + key + '\" does not match template'
    return 0

# validate_row() -------------------------------------------------------
# Validates a row in a csv file
# Params: row - the row to validate
#         days - regex for days
#         time - regex for time
#         date - regex for date
# Return: 0 if successful, error message if error
def validate_row(row, days, time, date):
    for key in row.keys():
        if row.get(key):
            row[key] = row.get(key).strip()
    # days should be formatted correctly
    if not days.match(row.get('Days')):
        return 'Days column not properly formatted'
    # start time should be formatted correctly or not exist
    if row.get('Start Time') != '' and not time.match(
        row.get('Start Time')):
        return 'Start time not properly formatted'
    # end time should be formatted correctly or not exist
    if row.get('End Time') != '' and not time.match(
        row.get('End Time')):
        return 'End time not properly formatted'
    # start date should be formatted correctly or not exist
    if row.get('Start Date') != '' and not date.match(
        row.get('Start Date')):
        return 'Start date not properly formatted'
    # end date should be formatted correctly or not exist
    if row.get('End Date') != '' and not date.match(
        row.get('End Date')):
        return 'End date not properly formatted'
    return 0

# bulk_update() --------------------------------------------------------
# Reads a CSV file and updates the database with the information
# Params: filename - a string containing the name of the file to
#           read from
# Return: a tuple containing a status code and a list of messages
#           if success - (0, [])
#           if error - (1, [])
def bulk_update(filename):
    error_messages = []
    try:
        with sqlalchemy.orm.Session(engine) as session:
            # clear all tables
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
            
            # open csv and ignore non utf-8 characters
            with open(filename, 'r', encoding='utf-8',
                errors='ignore') as csv_file:
                # read csv file as a list of dictionaries
                csv_reader = list(csv.DictReader(csv_file))

                # validate file
                val = validate_file(csv_reader)
                if val != 0:
                    return (2, ['File failed to upload due to the '
                        'error: ' + str(val)])

                # compile regexes to check rows
                days_regex = re.compile(
                    r'^[TF]-[TF]-[TF]-[TF]-[TF]-[TF]-[TF]$')
                time_regex = re.compile(
                    r'^0?([0-9]|1[0-9]|2[0-3]):[0-5][0-9]$')
                date_regex = re.compile(
                    r'^(1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])/'
                    '[0-9]{4}$')

                # initialize counters (efficiency purposes)
                organizations = 0
                offerings = 0
                services = 0
                groups = 0

                # iterate through each row in the csv file
                for row in csv_reader:
                    # validate row and skip if invalid
                    val = validate_row(row, days_regex, time_regex,
                        date_regex)
                    if val != 0:
                        error_str = 'Error on row ' + str(
                            csv_reader.index(row) + 1) + ': ' + str(val)
                        error_messages.append(error_str)
                        continue

                    #---------------------------------------------------
                    # Add to services table and group table
                    #---------------------------------------------------
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

                    #---------------------------------------------------
                    # Add to organizations table
                    #---------------------------------------------------
                    query = session.query(Organization.org_id) \
                        .filter(Organization.org_name.ilike(
                        row.get('Organization')))
                    res = query.first()

                    # if organization not in database, add it, else
                    # save the org_id
                    if not res:
                        organizations += 1
                        insert_stmt = text('INSERT INTO organizations '
                            '(org_name, phone, website, photo_url, '
                            'street, zip_code) VALUES (:org_name, '
                            ':phone, :website, :photo_url, :street, '
                            ':zip_code)')
                        session.execute(insert_stmt, {
                            'org_name': row.get('Organization'),
                            'phone': row.get('Phone Number'),
                            'website': row.get('Website'),
                            'street': row.get('Street'),
                            'zip_code': row.get('Zip Code'),
                            'photo_url': row.get('Photo URL')
                        })
                        org_id = organizations
                    else:
                        org_id = res[0]
                    
                    #---------------------------------------------------
                    # Add to offering table
                    #---------------------------------------------------
                    ins_off_stmt = text('INSERT INTO offerings '
                        '(title, days_open, days_desc, start_time, '
                        'end_time, init_date, close_date, off_service, '
                        'group_served, off_desc) VALUES '
                        '(:title, :days_open, :days_desc, :start_time, '
                        ':end_time, :init_date, :close_date, '
                        ':off_service, :group_served, :off_desc)')
                    
                    # replace with default values
                    if row.get('Title') == '':
                        row['Title'] = row.get('Organization')
                    # replace empty cells with None
                    for key in row:
                        if row[key] == '':
                            row[key] = None
                    # use default values for start and end time
                    if row.get('Start Time') == None:
                        row['Start Time'] = '00:00'
                    if row.get('End Time') == None:
                        row['End Time'] = '23:59'
                    # switch dates to postgres format
                    # YYYY-MM-DD
                    if row.get('Start Date'):
                        temp = row.get('Start Date').split('/')
                        month = str(temp[0]).zfill(2)
                        date = str(temp[1]).zfill(2)
                        row['Start Date'] = temp[2] + '-' + month + \
                            '-' + date
                    else:
                        row['Start Date'] = '1970-01-01'
                        print('default')
                    if row.get('End Date'):
                        temp = row.get('End Date').split('/')
                        month = str(temp[0]).zfill(2)
                        date = str(temp[1]).zfill(2)
                        row['End Date'] = temp[2] + '-' + month + \
                            '-' + date
                    else:
                        row['End Date'] = '9999-12-31'

                    # insert offering into database
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

                    #---------------------------------------------------
                    # Add to ownership table
                    #---------------------------------------------------
                    own_ins_stmt = text('INSERT INTO org_ownership '
                        '(org_id, off_id) VALUES (:org_id, :off_id)')
                    session.execute(own_ins_stmt, {
                        'org_id': org_id,
                        'off_id': offerings
                    })

            session.commit()

    except Exception as ex:
        print(ex, file=sys.stderr)
        return (1, ['File failed to upload due to an internal error.'])

    # return error messages
    error_messages.append('Successfully added ' + str(offerings) + 
        ' offerings!')
    return (0, error_messages)

if __name__ == '__main__':
    print('testing database.py')
    bulk_update('input-sample.csv')
