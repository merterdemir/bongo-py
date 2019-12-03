import argparse

def parameter_parser():
    parser = argparse.ArgumentParser(description = "Python API for BONGO (Bus On the GO).")

    parser.add_argument("-s", "--stop",
                        type = str,
                        nargs = 1,
                        default = None,
	                    help = "List the incoming buses for the given stop number.")
    
    parser.add_argument("-f", "--filter",
                        type = str,
                        nargs = 1,
                        default = None,
	                    help = "Filter the list according to given specification. This specification "\
                               "may be either a route tag like 'courthill' or an agency tag like "\
                               "'coralville' or 'iowa-city'. "\
                               "To see the tags run: "\
                               "\t ./bongo.py -t route or ./bongo.py -t agency")
    
    parser.add_argument("-l", "--list",
                        type = str,
                        nargs = 1,
                        default = None,
	                    help = "List all of the stops for a given route tag. "\
                               "To see the tags run: "\
                               "\t ./bongo.py -t route or ./bongo.py -t agency")

    parser.add_argument("-t", "--tags",
                        type = int,
                        nargs = 1,
                        default = 0,
                        choices=[0,1],
                        help = "If tags argument passed as 1, it will print the name->tag mappings for "\
                               "all routes and agencies.")

    return parser.parse_args()