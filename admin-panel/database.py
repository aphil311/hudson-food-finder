#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Authors: Aidan Phillips, Yousef Amin
#-----------------------------------------------------------------------

import sqlite3
import contextlib
import sys
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
        with sqlite3.connect(_DATABASE_URL_, isolation_level=None,
            uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute(stmt_str, args)
                table = cursor.fetchall()
                return table
    except Exception as ex:
        print(ex, file=sys.stderr)

#-----------------------------------------------------------------------
# find_offerings()
# Parameters: sort - a string containing the column to sort by
#             filter - a tuple with one string for each column we want
#                      to filter by
# Returns: a list of offering objects
#-----------------------------------------------------------------------
def find_offerings(filter):
    # SELECT
    stmt_str = 'SELECT public_organizations.org_name, '
    stmt_str += 'public_offerings.title, public_offerings.days_open, '
    stmt_str += 'public_offerings.start_time, '
    stmt_str += 'public_offerings.end_time, '
    stmt_str += 'public_offerings.init_date, '
    stmt_str += 'public_offerings.close_date, '
    stmt_str += 'public_services.service_type, '
    stmt_str += 'public_people_groups.people_group, '
    stmt_str += 'public_offerings.off_desc '
    stmt_str += 'FROM public_ownership, public_offerings, '
    stmt_str += 'public_organizations, public_services, '
    stmt_str += 'public_people_groups '
    stmt_str += 'WHERE public_ownership.org_id = '
    stmt_str += 'public_organizations.org_id AND '
    stmt_str += 'public_ownership.off_id = public_offerings.off_id AND '
    stmt_str += 'public_offerings.off_service = '
    stmt_str += 'public_services.service_id AND '
    stmt_str += 'public_offerings.group_served = '
    stmt_str += 'public_people_groups.group_id AND '
    stmt_str += 'public_organizations.org_name LIKE ?'

    # Execute query
    table = query(stmt_str, filter)

    # create offering objects and put them in a list
    offerings = []
    for row in table:
        offerings.append(offmod.Offering(row))
    return offerings

if __name__ == '__main__':
    # testing code
    find_offerings(('%', 'start_time'))
