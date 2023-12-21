#!/usr/bin/env python

from __future__ import print_function

import sys

sys.path.append( "..")
import   pypacker

org = [ "1234", "222"]

# ------------------------------------------------------------------------
# Test harness

if __name__ == '__main__':

    pb = pypacker.packbin()

    ddd = pb.encode_data("", org)
    ggg = pb.decode_data(ddd)

    if not org == ggg[0]:
        print ("Broken decode")
        sys.exit (1)
    else:
        print ("Compare OK")

# EOF