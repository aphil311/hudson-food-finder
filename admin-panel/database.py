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
import offering as offmod

#-----------------------------------------------------------------------
_DATABASE_URL_ = config('DB_URL')
#-----------------------------------------------------------------------

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
    # SELECT
    stmt_str = 'SELECT organizations.org_name, '
    stmt_str += 'offerings.title, offerings.days_open, '
    stmt_str += 'offerings.start_time, '
    stmt_str += 'offerings.end_time, '
    stmt_str += 'offerings.init_date, '
    stmt_str += 'offerings.close_date, '
    stmt_str += 'services.service_type, '
    stmt_str += 'people_groups.people_group, '
    stmt_str += 'offerings.off_desc '
    # FROM
    stmt_str += 'FROM org_ownership, offerings, '
    stmt_str += 'organizations, services, '
    stmt_str += 'people_groups '
    # WHERE
    stmt_str += 'WHERE org_ownership.org_id = '
    stmt_str += 'organizations.org_id AND '
    stmt_str += 'org_ownership.off_id = offerings.off_id AND '
    stmt_str += 'offerings.off_service = '
    stmt_str += 'services.service_id AND '
    stmt_str += 'offerings.group_served = '
    stmt_str += 'people_groups.group_id AND '
    # Allow for search by organization name
    stmt_str += 'organizations.org_name LIKE %s'

    # Execute query
    table = query(stmt_str, filter)

    # create offering objects and put them in a list
    offerings = []
    for row in table:
        offerings.append(offmod.Offering(row))
    return offerings

#-----------------------------------------------------------------------
# bulk_update()
# Reads a CSV file and updates the database with the information
# Parameters: filename - a string containing the name of the file to
#                        read from
# Returns: 0 if successful, 1 if not
#-----------------------------------------------------------------------
def bulk_update(filename):
    # Truncate tables so we can insert new data
    exe_stmt('TRUNCATE offerings RESTART IDENTITY CASCADE', ())
    exe_stmt('TRUNCATE org_ownership RESTART IDENTITY CASCADE', ())
    try:
        with open(filename, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # skip header row
                if line_count != 0:
                    inputs = []
                    inputs2 = []
                    # create new offering
                    stmt_str = 'INSERT INTO offerings ('
                    stmt_str += 'title, days_open, days_desc, '
                    stmt_str += 'start_time, '
                    stmt_str += 'end_time, init_date, close_date, '
                    stmt_str += 'off_service, group_served, off_desc)'
                    stmt_str += 'VALUES ('
                    stmt_str += '%s, %s, %s, %s, %s, %s, %s, %s, %s, '
                    stmt_str += '%s)'
                    # relate organization to offering
                    stmt_str2 = 'INSERT INTO org_ownership ('
                    stmt_str2 += 'org_id, off_id) VALUES ('
                    stmt_str2 += '%s, %s)'
                    for i, item in enumerate(row):
                        # use first col to find org_id
                        if i == 0:
                            inputs2.append(item)
                            inputs2.append(line_count)
                        else:
                            inputs.append(str(item))
                    # execute statements
                    exe_stmt(stmt_str, inputs)
                    exe_stmt(stmt_str2, inputs2)
                line_count += 1
    except Exception as ex:
        print(ex, file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    # testing code
    # find_offerings(('%', 'start_time'))
    bulk_update('test.csv')
