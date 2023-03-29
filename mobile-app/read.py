#!/usr/bin/env python

#-----------------------------------------------------------------------
# read.py
# Authors: Aidan Phillips
# Reads the database and generates a list of offerings
#-----------------------------------------------------------------------

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import or_
import sys
import offering as offmod
from schema import Offering, Organization, Ownership
import psycopg2
from decouple import config

#-----------------------------------------------------------------------
_DATABASE_URL_ = config('DB_URL')
#-----------------------------------------------------------------------

def find_offerings(filter):
    try:
        engine = sqlalchemy.create_engine('postgresql://',
            creator=lambda: psycopg2.connect(_DATABASE_URL_))
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Organization.photo_url, Offering.title, Organization.street, Offering.days_open,
                        Offering.start_time, Offering.end_time) \
                .select_from(Organization) \
                .join(Ownership) \
                .join(Offering) \
                .filter(or_(Organization.street.ilike(f'%{filter}%')),
                        or_(Offering.off_desc.ilike(f'%{filter}%')),
                        or_(Offering.title.ilike(f'%{filter}%')),
                        or_(Organization.zip_code.ilike(f'%{filter}%')),
                        or_(Organization.org_name.ilike(f'%{filter}%')))

            # execute the query and return the results
            offerings = []
            results = query.all()
            for row in results:
                offerings.append(offmod.Offering(row))
            return offerings
    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

def main():
    find_offerings('')

if __name__ == '__main__':
    main()