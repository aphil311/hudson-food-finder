#!/usr/bin/env python

class org:

    def __init__(self, organization, org_id, photo_url, zipcode, phone, website):
        self._organization = organization
        self._id = org_id
        self._photo_url = photo_url
        self._zipcode = zipcode
        self._phone = phone
        self._website = website

    def get_organization(self):
        return self._organization

    def get_id(self):
        return self._id

    def get_photo_url(self):
        return self._photo_url

    def get_zipcode(self):
        return self._zipcode

    def get_phone(self):
        return self._phone

    def get_website(self):
        return self._website
