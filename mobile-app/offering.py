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
        # initialize all the properties
        # need to tie ids to actual values here
        self._org_id = properties[0]
        self._off_id = properties[1]
        self._service = properties[2]
        self._other_services = properties[3]
        self._people_group = properties[4]
        self._description = properties[5]

        # convert times from strings to time objects
        temp = properties[6]
        self._start_time = time(temp)
        temp = properties[7]
        self._end_time = time(temp)

        # convert dates from strings to date objects
        temp = properties[8].split('-')
        self._start_date = date(int(temp[2]), int(temp[0]),
            int(temp[1]))
        temp = properties[9].split('-')
        self._end_date = date(int(temp[2]), int(temp[0]),
            int(temp[1]))

        # should think deeply about how to implement this
        temp = properties[10].split('-')
        self._days = []
        for day in temp:
            if day == 'F':
                self._days.append(False)
            elif day == 'T':
                self._days.append(True)
            else:
                print('Error: invalid day value in database',
                      file=sys.stderr)
                self._days.append(None)

    #-------------------------------------------------------------------
    # getter methods
    #-------------------------------------------------------------------
    def get_org_id(self):
        return self._org_id

    def get_off_id(self):
        return self._off_id

    def get_service(self):
        return self._service

    def get_other_services(self):
        return self._other_services

    def get_people_group(self):
        return self._people_group

    def get_description(self):
        return self._description

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

    def get_start_date(self):
        return self._start_date

    def get_end_date(self):
        return self._end_date

    def get_days(self):
        return self._days

    #-------------------------------------------------------------------
    # formatted getter methods
    #-------------------------------------------------------------------
    def get_start_timef(self):
        return self._start_time.strftime('%I:%M %p')

    def get_end_timef(self):
        return self._end_time.strftime('%I:%M %p')

    def get_start_datef(self):
        return self._start_date.strftime('%A, %B %d, %Y')

    def get_end_datef(self):
        return self._end_date.strftime('%A, %B %d, %Y')

    def get_daysf(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']
        result = ''
        for i in range(7):
            if self._days[i]:
                result += days[i] + ', '
        return 'Every ' + result[:-2]
