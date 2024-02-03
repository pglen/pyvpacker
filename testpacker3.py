#!/usr/bin/env python

from __future__ import print_function

import os, sys, getopt, signal, select, string, time
import struct, stat, base64, random, zlib

import pypacker

# ------------------------------------------------------------------------
# Test harness

if __name__ == '__main__':

    rrr =  "mTQdnL51eKnblQflLGSMvnMKDG4XjhKa9Mbgm5ZY9YLd" \
            "/SxqZZxwyKc/ZVzCVwMxiJ5X8LdX3X5VVO5zq/VBWQ==" #+ "b" * 100000

    pb = pypacker.packbin();
    pb.verbose = 0

    #bindat = Random.new().read(64)
    #print("bindat64:\n", base64.b64encode(bindat))

    bindat = base64.b64decode(rrr)

    org = [ 33, "sub", 'd', "longer str here with \' and \" all crap",  33, 33333333.2,
                {"test": 1111, "test2": 1112, }, bindat, "a" * 2000000 ]

    xlen = 0
    for aa in org:
        try:
            xlen += len(aa)
        except:
            pass
    xlen /= 1000
    if pb.verbose > 0:
        print ("org:\n", org)

    #print(xlen)

    ttt = time.time()

    eeenc = pb.encode_data("", *org)
    if pb.verbose > 2:
        print("eeenc:\n", "{" + eeenc + "}")
    print ("encode ttt=%.2f kBytes/s" % (xlen / (time.time() - ttt)))

    ttt = time.time()
    dddec = pb.decode_data(eeenc)
    if pb.verbose > 1:
        print("dddec:\n",  "{" + str(dddec) + "}")

    print ("decode ttt=%.2f kBytes/s" % (xlen / (time.time() - ttt)))

    if org == dddec:
        #print("Data matches OK.")
        print("Match OK")
        pass
    else:
        print("MISMATCH:")


# EOF
