#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Authors: Aidan Phillips, Yousef Amin
#-----------------------------------------------------------------------

import contextlib
import sys
import psycopg2
from decouple import config
import offering as offmod

#-----------------------------------------------------------------------
_DATABASE_URL_ = config('DB_URL')
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# query()
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
# find_offerings()
# Parameters: sort - a string containing the column to sort by
#             filter - a tuple with one string for each column we want
#                      to filter by
# Returns: a list of offering objects
#-----------------------------------------------------------------------
def find_offerings(filter):
    query_str = 'SELECT * from offerings'
    inputs = []
    print(query(query_str, inputs))
    search_types = 5
    inputs = []
    # search term
    for _ in range(search_types):
        inputs.append('%' + filter[0] + '%')

    # SELECT
    stmt_str = 'SELECT organizations.photo_url, '
    stmt_str += 'offerings.title, '
    stmt_str += 'organizations.street, '
    stmt_str += 'offerings.days_open, '
    stmt_str += 'offerings.start_time, '
    stmt_str += 'offerings.end_time FROM '
    stmt_str += 'organizations, offerings, '
    stmt_str += 'org_ownership '
    stmt_str += 'WHERE org_ownership.off_id = '
    stmt_str += 'offerings.off_id AND '
    stmt_str += 'org_ownership.org_id = organizations.org_id '
    stmt_str += 'AND(organizations.street LIKE %s '
    stmt_str += 'OR offerings.off_desc LIKE %s '
    stmt_str += 'OR offerings.title LIKE %s '
    stmt_str += 'OR organizations.zip_code LIKE %s '
    stmt_str += 'OR organizations.org_name LIKE %s)'

    # Execute query
    table = query(stmt_str, inputs)

    # create offering objects and put them in a list
    offerings = []
    for row in table:
        offerings.append(offmod.Offering(row))
    return offerings

if __name__ == '__main__':
    # testing code
    find_offerings(('%', 'offerings.start_time'))
