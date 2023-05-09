#!/usr/bin/env python

#-----------------------------------------------------------------------
# offering.py
# Authors: Aidan Phillips
# Represents an offering in the database
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# Organization class
# Represents an organization in the database
#-----------------------------------------------------------------------
class Organization:
    #-------------------------------------------------------------------
    # __init__()
    # Constructor for the offering class
    # Parameters: properties - a list of raw properties pulled directly
    #                          from the database
    #-------------------------------------------------------------------
    def __init__(self, properties):
        self._org_name = properties[0]
        self._phone = properties[1]
        self._website = properties[2]
        self._street = properties[3]
        self._zip_code = properties[4]
        self._id = properties[5]
        self._photo_url = properties[6]

    #-------------------------------------------------------------------
    # getter methods
    #-------------------------------------------------------------------
    def get_org_name(self):
        return self._org_name
    def get_phone(self):
        return self._phone
    def get_website(self):
        return self._website
    def get_photo_url(self):
        return self._photo_url
    def get_street(self):
        return self._street
    def get_id(self):
        return self._id
