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
        self._title = properties[1]
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
        temp = properties[4].split(':')
        self._start_time = time(int(temp[0]), int(temp[1]))
        temp = properties[5].split(':')
        self._end_time = time(int(temp[0]), int(temp[1]))

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
        return self._start_time.strftime('%I:%M %p')

    def get_end_timef(self):
        return self._end_time.strftime('%I:%M %p')

    def get_daysf(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']
        result = ''
        for i in range(7):
            if self._days[i]:
                result += days[i] + ', '
        return 'Every ' + result[:-2]
