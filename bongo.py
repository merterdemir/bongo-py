#! /usr/bin/env python3

import sys
import requests
import numpy as np
from parser import parameter_parser
from astropy.table import Table, Column

def print_tag_table(table_dict):
    route_table  = Table(names=('Route Name', 'Route Tag'), dtype=('S', 'S'))
    agency_table = Table(names=('Agency Name', 'Agency Tag'), dtype=('S', 'S'))
    #print(table_dict['routes'])
    for (name, tag) in table_dict['routes'].items():
        route_table.add_row((name, tag))
    for name, tag in table_dict['agencies'].items():
        agency_table.add_row((name, tag))

    print("")
    route_table.pprint_all(align="<")
    print("")
    agency_table.pprint_all(align="<")

def get_tag_mapping():
    tag_table = {'routes': {}, "agencies": {}}
    all_req   = requests.get("https://api.ebongo.org/routelist?api_key=XXXX")
    if all_req.status_code != 200:
        print("Problem related with API. Try again later.")
        return
    all_req = all_req.json()
    try:
        for route in all_req['routes']:
            route_name  = route['route']['name']
            route_tag   = route['route']['tag']
            agency_tag  = route['route']['agency']
            agency_name = route['route']['agencyname']
            tag_table['routes'][route_name]  = route_tag
            tag_table['agencies'][agency_name] = agency_tag
        print_tag_table(tag_table)
    except Exception as e:
        print("Problem while accessing the routes. Try again later:", e)
        return

def main(args):
    if args.tags:
        get_tag_mapping()
    else:
        pass

if (__name__ == "__main__"):
    args = parameter_parser()
    main(args)