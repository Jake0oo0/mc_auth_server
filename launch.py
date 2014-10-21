#!/usr/bin/env python

import os, imp

def main(args):
    if len(args) == 0:
        print "Usage: python launch.py [args...]"
        return

    launch_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "auth_server.py")

    auth_server = imp.load_source("auth_server", launch_path)
    auth_server.main(args)

if __name__ == '__main__':
    import sys
    main(sys.argv)