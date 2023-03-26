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
    stmt_str = 'SELECT * FROM public_offerings '
    # WHERE
    stmt_str += 'WHERE service LIKE ? AND '
    stmt_str += 'days LIKE ? AND '
    stmt_str += 'start_time LIKE ? AND '
    stmt_str += 'end_time LIKE ? AND '
    stmt_str += 'people_group LIKE ? AND '
    stmt_str += 'other_services LIKE ? '
    # ORDER BY
    stmt_str += 'ORDER BY ?'

    # Execute query
    table = query(stmt_str, filter)

    # create offering objects and put them in a list
    offerings = []
    for row in table:
        offerings.append(offmod.Offering(row))
    return offerings

if __name__ == '__main__':
    # testing code
    find_offerings(('%', '%', '%', '%', '%', '%', 'start_time'))
