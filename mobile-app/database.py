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
from schema import Service, Group

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
    services = filter[2]
    days = filter[3]
    day_query = []
    # query tamplate
    template = '_-_-_-_-_-_-_'
    term = 'offerings.days_open LIKE ('
    # split days into a list where each day is a separate element
    days = days.split('-')
    for x in range(len(days)):
        if days[x] == 'T':
            temp = term + "'" + template[:x*2] + 'T' + template[x*2+1:] + "')"
            day_query.append(sqlalchemy.text(temp))

    if len(day_query) == 0:
        day_query.append(sqlalchemy.text(term + "'_-_-_-_-_-_-_')"))

    times = filter[4]
    groups = filter[5]
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
                        (Service.service_type.in_(services))) \
                .filter(sqlalchemy.or_(*day_query)) \
                .filter((Offering.start_time < times[1]) &
                        (Offering.end_time > times[0])) \
                .filter((Group.group_id == Offering.group_served) &
                        (Group.people_group.in_(groups))) \
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

def get_services():
    try:
        # connect to the database
        with sqlalchemy.orm.Session(engine) as session:
            # form the query
            query = session.query(Service.service_type) \
                .distinct() \
                .filter(Service.service_type != '') \
                .order_by(Service.service_type)

            # execute the query and return the results
            results = query.all()
            services = []
            for row in results:
                services.append(row[0])
            return services
    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

def get_groups():
    try:
        # connect to the database
        with sqlalchemy.orm.Session(engine) as session:
            # form the query
            query = session.query(Group.people_group) \
                .distinct() \
                .filter(Group.people_group != '') \
                .order_by(Group.people_group)

            # execute the query and return the results
            results = query.all()
            groups = []
            for row in results:
                groups.append(row[0])
            return groups
    except Exception as ex:
        print(ex, file=sys.stderr)
        return None

# Test function
def main():
    # find_offerings('')
    services = get_services()
    for service in services:
        print(service)
    groups = get_groups()
    for group in groups:
        print(group)

if __name__ == '__main__':
    main()
