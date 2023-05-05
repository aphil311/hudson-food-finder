#!/usr/bin/env python

#-----------------------------------------------------------------------
# offering.py
# Authors: Aidan Phillips
# Represents an offering in the database
#-----------------------------------------------------------------------

from datetime import date
from datetime import time
import sys

#-----------------------------------------------------------------------
# Offering class
# Represents an offering in the database
#-----------------------------------------------------------------------
class Offering:
    #-------------------------------------------------------------------
    # __init__()
    # Constructor for the offering class
    # Parameters: properties - a list of raw properties pulled directly
    #                          from the database
    #-------------------------------------------------------------------
    def __init__(self, properties):
        self._org = properties[0]
        self._title = properties[1]
        if self._title == '':
            self._title = self._org

        # convert days_open from a string to a list of booleans
        temp = properties[2].split('-')
        self._days_open = []
        for day in temp:
            if day == 'F':
                self._days_open.append(False)
            elif day == 'T':
                self._days_open.append(True)
            else:
                print('Error: invalid day value in database',
                      file=sys.stderr)
                self._days_open.append(None)

        # convert start_time and end_time from strings to time objects
        if properties[3]:
            self._start_time = properties[3]
        else:
            self._start_time = time(0, 0)
        if properties[4]:
            self._end_time = properties[4]
        else:
            self._end_time = time(23, 59)

        # convert init_date and close_date from strings to date objects
        if properties[5]:
            self._init_date = properties[5]
        else:
            self._init_date = date(1, 1, 1)
        if properties[6]:
            self._close_date = properties[6]
        else:
            self._close_date = date(1, 1, 1)

        self._service = properties[7]
        self._people_group = properties[8]
        self._description = properties[9]
        self._id = properties[10]

    #-------------------------------------------------------------------
    # getter methods
    #-------------------------------------------------------------------
    def get_id(self):
        return self._id
    def get_org(self):
        return self._org
    def get_title(self):
        return self._title
    def get_days_open(self):
        return self._days_open
    def get_start_time(self):
        return self._start_time
    def get_end_time(self):
        return self._end_time
    def get_init_date(self):
        return self._init_date
    def get_close_date(self):
        return self._close_date
    def get_service(self):
        return self._service
    def get_people_group(self):
        return self._people_group
    def get_description(self):
        return self._description

    #-------------------------------------------------------------------
    # formatted getter methods
    #-------------------------------------------------------------------
    def get_start_timef(self):
        return self._start_time.strftime('%I:%M %p')

    def get_end_timef(self):
        return self._end_time.strftime('%I:%M %p')

    def get_start_datef(self):
        if self._init_date == date(1970, 1, 1):
            return 'N/A'
        return self._init_date.strftime('%m/%d/%y')

    def get_end_datef(self):
        if self._close_date == date(9999, 12, 31):
            return 'N/A'
        if type(self._close_date) == str:
            print(self._close_date)
        return self._close_date.strftime('%m/%d/%y')

    def get_days_openf(self):
        days = ['Su', 'M', 'Tu', 'W', 'Th', 'F', 'Sa']
        result = ''
        for i in range(7):
            if self._days_open[i]:
                result += days[i] + ', '
        return result[:-2]
