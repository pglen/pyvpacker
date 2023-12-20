#!/usr/bin/env python

from __future__ import print_function

import os, sys, getopt, signal, select, string, time
import struct, stat, base64, random, zlib

from Crypto import Random
from Crypto.Hash import SHA512

import  pypacker

# {pg s7 'iscsifd' i4 33 s3 'sub' c1 d s37
# 'longer str here with ' and " all crap' i4 33 f8 33333333.200000
# d101 'pg s1 'a' a84 'pg s2 'tt' t29 'pg s2 'si' s4 'test' i4 1111 ' t30 'pg s2 'si' s5 'test2' i4 1112 ' ' ' }

# ------------------------------------------------------------------------
# Test harness

if __name__ == '__main__':

    pb = pypacker.packbin();
    pb.verbose = 4
    pb.pgdebug = 0

    org  = [b'12345',]

    # did not know this is not equal
    #org2 = ( org2, "hrllo", [b'123',], ("aa", "bb") )
    #print("cmp:", org == org2)

    if pb.verbose > 2:
        print ("org:\n", org)

    eeenc = pb.encode_data("", *org)
    if pb.verbose > 2:
        print("eeenc:\n", eeenc )

    #eeenc = eeenc[:16] + "x" + eeenc[17:]
    #print("part", eeenc)

    dddec = pb.decode_data(eeenc)
    if pb.verbose > 2:
        print("dddec:\n",   str(dddec) )

    if org == dddec:
        print("Data matches OK.")
        pass
    else:
        print("MISMATCH:", dddec[0])
        sys.exit(1)

    sys.exit(0)

    #print ("Should print 3 successes")
    #iscsifb
    #eee = pb.encode_data("iscsfb", *org)

    eee = pb.encode_data("", *org)
    if pb.verbose > 2:
        print ("eee:\n", eee)

    ddd = pb.decode_data(eee)
    if pb.verbose > 2:
        print ("ddd:\n", ddd)

    if not org == ddd:
        print ("Broken decode")
        print ("eee:\n", eee)
    else:
        pass
        #print ("Success1 ", end="")

    org2 = [ 22, 444, "data", 123.456, 'a', eee]
    #print ("org2:\n", org2)
    #eee2 = pb.encode_data("ilsfcx", *org2)
    eee2 = pb.encode_data("ilsfcx", *org2)
    #print ("eee2:\n", eee2)
    ddd2 = pb.decode_data(eee2)
    #print ("ddd2:\n", ddd2)

    if not org2 == ddd2:
        print ("Broken decode")
        print ("eee2:\n", eee2)
    else:
        pass
        #print ("Success2 ", end="")

    if sys.version_info[0] > 2:
        eee  = eee.encode("cp437")

    fff = zlib.compress(eee)

    #print("compressed %.2f" % (float(len(fff)) / len(eee)) )

    hhh = zlib.decompress(fff)
    if not eee == hhh:
        print ("Broken unzip")
    else:
        pass
        #print("Unzip OK")

    ddd3 = pb.decode_data(eee2)
    #print("ddd3", ddd3)
    ggg = pb.decode_data(ddd3[5])
    #print("ggg", ggg)

    if not org == ggg :
        print ("Broken decode")
        sys.exit(1)
    else:
        print ("Success, compare OK")

# EOF