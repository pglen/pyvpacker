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

compz = ["12340-9540987sdkljsdfakjbsdfkbds", [varp],
                ["jfaskljhfsdkljfdskjlsadfdasd"], "dsadsdd"]

def test_enc_dec(capsys):

    ddd = packer.encode_data("", compz)
    dec = packer.decode_data(ddd)
    assert compz == dec[0]

def test_compz(capsys):

    ddd = packer.encode_data("", compz)
    eee = "pg s1 'a' a140 'pg s4 'saas' s32 '12340-9540987sdkljsdfakjbsdfkbds' " \
    "a16 'pg s1 'i' i4 12 ' a45 'pg s1 's' s28 " \
    "'jfaskljhfsdkljfdskjlsadfdasd' ' s7 'dsadsdd' ' "

    #print (eee)
    #assert 0

    assert ddd == eee
    dec = packer.decode_data(ddd)
    assert compz == dec[0]



# EOF
