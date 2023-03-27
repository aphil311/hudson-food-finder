#!/usr/bin/env python

#-----------------------------------------------------------------------
# offering.py
# Authors: Aidan Phillips
# Represents an offering in the database
#-----------------------------------------------------------------------

from datetime import date
from datetime import time
import sys

class Offering:
    #-------------------------------------------------------------------
    # __init__()
    # Parameters: properties - a list of raw properties pulled directly
    #                          from the database
    #-------------------------------------------------------------------
    def __init__(self, properties):
        self._org = properties[0]
        self._title = properties[1]
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

        temp = properties[3].split(':')
        self._start_time = time(int(temp[0]), int(temp[1]))
        temp = properties[4].split(':')
        self._end_time = time(int(temp[0]), int(temp[1]))

        temp = properties[5].split('-')
        self._init_date = date(int(temp[2]), int(temp[0]),
            int(temp[1]))

        if properties[6]:
            temp = properties[6].split('-')
            self._close_date = date(int(temp[2]), int(temp[0]),
                int(temp[1]))
        else:
            self._close_date = date(1, 1, 1)

        self._service = properties[7]
        self._people_group = properties[8]
        self._description = properties[9]

    #-------------------------------------------------------------------
    # getter methods
    #-------------------------------------------------------------------
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
        return self._init_date.strftime('%m/%d/%y')

    def get_end_datef(self):
        if self._close_date == date(1, 1, 1):
            return 'indefinite'
        return self._close_date.strftime('%m/%d/%y')

    def get_days_openf(self):
        days = ['M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su']
        result = ''
        for i in range(7):
            if self._days_open[i]:
                result += days[i] + ', '
        return result[:-2]
