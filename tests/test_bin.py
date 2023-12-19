#!/usr/bin/env python3

import pytest, os, sys
from mytest import *
import pypacker

# Test for pydbase

packer = None

def setup_module(module):
    """ setup any state specific to the execution of the given module."""

    global packer
    packer = pypacker.packbin()

    try:
        # Fresh start
        pass
    except:
        #print(sys.exc_info())
        pass

org2 = b""
for aa in range(5, 15):
    org2 += str(aa).encode("utf-8")

org = ["abcd", org2, [1234, ] ]

def test_packer(capsys):

    ddd = packer.encode_data("", org)
    out =   "pg s1 'a' a74 'pg s3 'sba' s4 'abcd' b20 'NTY3ODkxMDExMTIxMzE0' " \
            "a18 'pg s1 'i' i4 1234 ' ' "
    assert ddd == out

def test_enc_dec(capsys):

    ddd = packer.encode_data("", org)
    dec = packer.decode_data(ddd)
    assert org == dec[0]


# EOF
