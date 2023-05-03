#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Authors: Aidan Phillips, Zain Ahmed, Yousef Amin
# Starts the server
#-----------------------------------------------------------------------

import argparse
import sys
import wsgiref.simple_server as wss
import app as hcff

#-----------------------------------------------------------------------
# main()
# Parameters: none
# Returns: nothing
# Handles command line arguments and starts the server
#-----------------------------------------------------------------------
def main():

    # Google expects the server to be running on port 5000
    PORT = 5000

    # handle arguments
    
    parser = argparse.ArgumentParser(
        description='The admin panel application')
    parser.parse_args()

    if len(sys.argv) != 1:
        print("Usage: " + sys.argv[0], file = sys.stderr)


    try:
        hcff.app.run(host='localhost', port = PORT, debug = True, 
            ssl_context = ('cert.pem', 'key.pem'))
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)



    # try:
    #     httpd = wss.make_server('0.0.0.0', PORT, app.app, 
    #         ssl_context = ('cert.pem', 'key.pem'))
    #     print('Listening on port', PORT, '...')
    #     httpd.serve_forever()
    # except Exception as ex:
    #     print(ex, file=sys.stderr)
    #     sys.exit(1)

if __name__ == '__main__':
    main()