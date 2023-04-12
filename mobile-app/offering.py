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
        if self._photo_url == None:
            self._photo_url = './static/img/fallback.png'
        self._title = properties[1]
        if self._title == '':
            self._title = properties[6]
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
        if (properties[4]):
            temp = properties[4].split(':')
            self._start_time = time(int(temp[0]), int(temp[1]))
        else:
            self._start_time = time(0, 0)
        if  (properties[5]):
            temp = properties[5].split(':')
            self._end_time = time(int(temp[0]), int(temp[1]))
        else:
            self._end_time = time(23, 59)

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

    #-------------------------------------------------------------------
    # formatted getter methods
    #-------------------------------------------------------------------
    def get_start_timef(self):
        return self._start_time.strftime('%-I:%M %p')

    def get_end_timef(self):
        return self._end_time.strftime('%-I:%M %p')

    def get_daysf(self):
        if self._days == [True, True, True, True, True, True, True]:
            return 'Open every day'
        if self._days == [False, True, True, True, True, True, False]:
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
