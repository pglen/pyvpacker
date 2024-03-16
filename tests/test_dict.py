#!/usr/bin/env python3

import pytest, os, sys
from mytest import *
import pyvpacker

# Test for pydbase

packer = None

def setup_module(module):
    """ setup any state specific to the execution of the given module."""

    global packer
    packer = pyvpacker.packbin()

    try:
        # Fresh start
        pass
    except:
        #print(sys.exc_info())
        pass

varp = 12

dictz = [ {"z123409540987sdkljsdfakjbsdfkbds": varp},
                ["jfaskljhfsdkljfdskjlsadfdasd"], "dsadsdd"]

def test_dictz(capsys):

    ddd = packer.encode_data("", dictz)
    eee = \
        "pg s1 'a' a174 'pg s3 'das' d90 'pg s1 'a' a73 "\
        "'pg s1 't' t56 'pg s2 'si' s32 'z123409540987sdkljsdfakjbsdfkbds'"\
        " i4 12 ' ' ' a45 'pg s1 's' s28 'jfaskljhfsdkljfdskjlsadfdasd' '"\
        " s7 'dsadsdd' ' "

    assert ddd == eee
    dec = packer.decode_data(ddd)
    assert dictz == dec[0]

# EOF
