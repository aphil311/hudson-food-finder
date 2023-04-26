#!/usr/bin/env python

#-----------------------------------------------------------------------
# read.py
# Authors: Aidan Phillips
# Reads the database and generates a list of offerings
#-----------------------------------------------------------------------

import sys
import sqlalchemy
import sqlalchemy.orm
import init
import offering as offmod
from schema import Offering, Organization, Ownership
from schema import Service

engine = init.engine

#-----------------------------------------------------------------------
# find_offerings()
# Returns a list of offerings based on the search term and sort by
# parameters
# Parameters: filter - a tuple containing the search term and sort by
# Returns: a list of offerings
#-----------------------------------------------------------------------
def find_offerings(filter):
    search_term = '%' + filter[0] + '%'
    sort_by = filter[1]
    service_name_1 = 'Shelter'
    service_name_2 = 'Food Pantry'
    try:
        # connect to the database
        with sqlalchemy.orm.Session(engine) as session:
            # form the query
            query = session.query(Organization.photo_url,
                Offering.title, Organization.street, Offering.days_open,
                Offering.start_time, Offering.end_time,
                Organization.org_name, Offering.off_id,
                Offering.off_desc) \
                .select_from(Organization) \
                .join(Ownership) \
                .join(Offering) \
                .filter(Organization.street.ilike(search_term) |
                        Offering.off_desc.ilike(search_term) |
                        Offering.title.ilike(search_term) |
                        Organization.zip_code.ilike(search_term) |
                        Organization.org_name.ilike(search_term)) \
                .filter((Service.service_id == Offering.off_service) &
                        ((Service.service_type.ilike(service_name_1)) |
                        (Service.service_type.ilike(service_name_2)))) \
                .order_by(sqlalchemy.text(sort_by))

            # execute the query and return the results
            results = query.all()
            offerings = []
            for row in results:
                offerings.append(offmod.Offering(row))
            return offerings
    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

#-----------------------------------------------------------------------
def get_offering(id):
    try:
        # connect to the database
        with sqlalchemy.orm.Session(engine) as session:
            # form the query
            query = session.query(Organization.photo_url,
                Offering.title, Organization.street, Offering.days_open,
                Offering.start_time, Offering.end_time,
                Organization.org_name, Offering.off_id,
                Offering.off_desc) \
                .select_from(Organization) \
                .join(Ownership) \
                .join(Offering) \
                .filter(Offering.off_id == id)

            # execute the query and return the results
            results = query.all()
            if results is None:
                return None
            else:
                return offmod.Offering(results[0])

    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

# Test function
def main():
    find_offerings('')

if __name__ == '__main__':
    main()
