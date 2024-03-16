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
org =  [ {"www" :  111}, {"eee" : 222}, 1234, "abcd", [1,2,3,4] ]

def test_packer(capsys):

    ddd = packer.encode_data("", org)
    print(ddd)
    captured = capsys.readouterr()

    out =  "pg s1 'a' a208 'pg s5 'ddisa' d61 'pg s1 'a' a44 'pg s1 't' " \
    "t27 'pg s2 'si' s3 'www' i4 111 ' ' ' d61 'pg s1 'a' a44 'pg s1 " \
    "'t' t27 'pg s2 'si' s3 'eee' i4 222 ' ' ' i4 1234 s4 'abcd' a33 'pg s4"\
    " 'iiii' i4 1 i4 2 i4 3 i4 4 ' ' \n"

    assert captured.out == out

def test_enc_dec(capsys):

    ddd = packer.encode_data("", org)
    dec = packer.decode_data(ddd)
    assert org == dec[0]

# EOF
