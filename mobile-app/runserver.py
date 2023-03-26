#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Authors: Aidan Phillips
# Starts the server
#-----------------------------------------------------------------------

import argparse
import sys
import wsgiref.simple_server as wss
import app

#-----------------------------------------------------------------------
# main()
# Parameters: none
# Returns: nothing
# Handles command line arguments and starts the server
#-----------------------------------------------------------------------
def main():
    # handle arguments
    parser = argparse.ArgumentParser(
        description='The mobile client application')
    parser.add_argument('port', type=int,
        help='the port at which the server should listen')
    args = parser.parse_args()
    port = args.port

    try:
        httpd = wss.make_server('0.0.0.0', port, app.app)
        print('Listening on port', port, '...')
        httpd.serve_forever()
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
