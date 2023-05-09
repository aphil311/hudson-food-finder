#!/usr/bin/env python

#-----------------------------------------------------------------------
# offering.py
# Authors: Aidan Phillips
# Represents an offering in the database
#-----------------------------------------------------------------------

from datetime import time
import sys

class Offering:
    #-------------------------------------------------------------------
    # __init__()
    # Parameters: properties - a list of raw properties pulled directly
    #                          from the database
    #-------------------------------------------------------------------
    def __init__(self, properties):
        self._photo_url = properties[0]
        if self._photo_url == '':
            self._photo_url = './static/img/fallback.png'
        self._title = properties[1]
        if self._title == '':
            self._title = properties[7]
        self._street = properties[2]
        # should think deeply about how to implement this
        temp = properties[3].split('-')
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
        self._days_desc = properties[4]
        if properties[5]:
            self._start_time = properties[5]
        else:
            self._start_time = time(0, 0)
        if properties[5]:
            self._end_time = properties[6]
        else:
            self._end_time = time(23, 59)

        self._off_id = properties[8]

        self._description = properties[9]
        if self._description is None:
            self._description = ''

        self._zipcode = properties[10]
        self._service = properties[11]
        self._group = properties[12]
        self._phone = properties[13]
        self._website = properties[14]

    #-------------------------------------------------------------------
    # getter methods
    #-------------------------------------------------------------------
    def get_photo_url(self):
        return self._photo_url

    def get_title(self):
        return self._title

    def get_street(self):
        return self._street

    def get_days(self):
        return self._days

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

    def get_description(self):
        return self._description

    def get_off_id(self):
        return self._off_id

    def get_zipcode(self):
        return self._zipcode

    def get_service(self):
        return self._service

    def get_group(self):
        return self._group

    def get_phone(self):
        return self._phone

    def get_website(self):
        return self._website

    #-------------------------------------------------------------------
    # formatted getter methods
    #-------------------------------------------------------------------
    def get_start_timef(self):
        return self._start_time.strftime('%-I:%M %p')

    def get_end_timef(self):
        return self._end_time.strftime('%-I:%M %p')

    def get_daysf(self):
        if self._days_desc:
            return self._days_desc
        if self._days == [True, True, True, True, True, True, True]:
            return 'Open every day'
        if self._days == [False, True, True, True, True, True,
            False]:
            return 'Open on weekdays'
        if self._days == [True, False, False, False, False, False,
            True]:
            return 'Open on weekends'
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday']
        result = ''
        for i in range(7):
            if self._days[i]:
                result += days[i] + ', '
        return 'Open every ' + result[:-2]
