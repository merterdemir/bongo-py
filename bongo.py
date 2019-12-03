#! /usr/bin/env python3

import sys
import requests
import numpy as np
from parser import parameter_parser
from astropy.table import Table, Column

def _print_tag_table(table_dict):
    route_table  = Table(names=('Route Tag', 'Route Name', 'Agency Name'), dtype=('S', 'S', 'S'))
    agency_table = Table(names=('Agency Name', 'Agency Tag'), dtype=('S', 'S'))
    for (tag, features) in sorted(table_dict['routes'].items()):
        route_table.add_row((tag, features[0], features[2]))
    for (name, tag) in sorted(table_dict['agencies'].items()):
        agency_table.add_row((name, tag))
    print("")
    route_table.pprint_all(align="<")
    print("")
    agency_table.pprint_all(align="<")
    print("")

def get_tag_mapping():
    tag_table = {'routes': {}, "agencies": {}}
    all_req   = requests.get("https://api.ebongo.org/routelist?api_key=XXXX")
    if all_req.status_code != 200:
        print("Problem related with API. Try again later.")
        return None
    try:
        all_req = all_req.json()
        for route in all_req['routes']:
            route_name  = route['route']['name']
            route_tag   = route['route']['tag']
            agency_tag  = route['route']['agency']
            agency_name = route['route']['agencyname']
            tag_table['routes'][route_tag]    = [route_name, agency_tag, agency_name]
            tag_table['agencies'][agency_name] = agency_tag
        return tag_table
    except Exception as e:
        print("Problem while accessing the routes. Try again later.", e)
        return None

def _fix_stop_id(stop_id):
    return "0" * (4 - len(str(stop_id))) + str(stop_id)

def _get_route_info(tag_table, route):
    try:
        assert tag_table['routes'][route]
        return [route] + tag_table['routes'][route]
    except Exception as e:
        print("Error while accessing route info.", e)
        return None

def _print_route_stops(route_info, stop_list):
    if not route_info or not stop_list:
        return None
    stop_table = Table(names=('Stop Number', 'Name'), dtype=('S', 'S'))
    for stop in stop_list:
        stop_table.add_row(stop)
    print("")
    print("--> Route:", route_info[1].upper(),"<--")
    stop_table.pprint_all(align="<")
    print("")

def get_stops(route_info):
    try:
        assert route_info
        stops   = []
        all_req = requests.get("https://api.ebongo.org/route?agency={}&route={}&api_key=XXXX".format(route_info[2], route_info[0]))
        if all_req.status_code != 200:
            print("Problem related with API. Try again later.")
            return None
        all_req = all_req.json()
        for stop in all_req['route']['directions'][0]['stops']:
            stop_id = _fix_stop_id(stop['stopnumber'])
            stops.append((stop_id, stop['stoptitle']))   
        return stops    
    except Exception as e:
        print("Problem with the route tag or stop id. Try again later.", e)
        return None

def _print_predictions(stop_id, predictions):
    pred_table = Table(names=('Minutes', 'Route', 'Agency'), dtype=('S', 'S', 'S'))
    if not predictions:
        pred_table.add_row(('-', '-', '-'))
    else:
        for pred in predictions:
            pred_table.add_row(pred[:3])
    print("")
    print("--> Stop:", stop_id, "<--")
    pred_table.pprint_all(align="<")
    print("")

def filter_predictions(predictions, filter):
    try:
        assert filter and predictions
        filter = filter[0]
        return [pred for pred in predictions if filter in pred[3]]
    except:
        return predictions

def get_predictions(stop_id, filter):
    try:
        predictions = []
        all_req = requests.get("https://api.ebongo.org/prediction?stopid={}&api_key=XXXX".format(stop_id))
        if all_req.status_code != 200:
            print("Problem related with API. Try again later.")
            return None
        all_req = all_req.json()
        for prediction in all_req["predictions"]:
            route       = prediction['title']
            agency      = prediction['agencyName']
            minutes     = prediction['minutes']
            route_tag   = prediction['tag']
            agency_tag  = prediction['agency']
            predictions.append((int(minutes), route, agency, [route_tag, agency_tag]))
        return filter_predictions(predictions, filter)
    except Exception as e:
        print("Problem with the predictions. Try again later.", e)
        return None

def main(args):
    tag_table = get_tag_mapping()
    if tag_table and args.tags and args.tags[0]:
        _print_tag_table(tag_table)
    else:
        if args.stop:
            stop_id     = _fix_stop_id(args.stop[0])
            predictions = get_predictions(stop_id, args.filter)
            _print_predictions(stop_id, predictions)
        elif args.list:
            route_tag  = args.list[0]
            route_info = _get_route_info(tag_table, route_tag)
            stops      = get_stops(route_info)
            _print_route_stops(route_info, stops)

if (__name__ == "__main__"):
    args = parameter_parser()
    main(args)