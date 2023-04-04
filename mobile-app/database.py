#!/usr/bin/env python

#-----------------------------------------------------------------------
# read.py
# Authors: Aidan Phillips
# Reads the database and generates a list of offerings
#-----------------------------------------------------------------------

import sys
import sqlalchemy
import sqlalchemy.orm
import psycopg2
from decouple import config
import offering as offmod
from schema import Offering, Organization, Ownership

#-----------------------------------------------------------------------
_DATABASE_URL_ = config('DB_URL')
#-----------------------------------------------------------------------

def find_offerings(filter):
    search_term = '%' + filter[0] + '%'
    sort_by = filter[1]
    try:
        engine = sqlalchemy.create_engine('postgresql://',
            creator=lambda: psycopg2.connect(_DATABASE_URL_))
        with sqlalchemy.orm.Session(engine) as session:
            query = session.query(Organization.photo_url,
                Offering.title, Organization.street, Offering.days_open,
                Offering.start_time, Offering.end_time) \
                .select_from(Organization) \
                .join(Ownership) \
                .join(Offering) \
                .filter(Organization.street.ilike(search_term) |
                        Offering.off_desc.ilike(search_term) |
                        Offering.title.ilike(search_term) |
                        Organization.zip_code.ilike(search_term) |
                        Organization.org_name.ilike(search_term)) \
                .order_by(sqlalchemy.text(sort_by))

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
