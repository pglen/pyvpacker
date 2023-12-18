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
    org2 += bytes(chr(aa), "utf-8")

org = ["abcd", org2, 1234 ]

def test_packer(capsys):

    ddd = packer.encode_data("", org)
    print(ddd)
    captured = capsys.readouterr()

    out = "pg s1 'a' a53 'pg s3 'sbi' s4 'abcd' b16 'BQYHCAkKCwwNDg==' i4 1234 ' \n"

    assert captured.out == out

def test_enc_dec(capsys):

    ddd = packer.encode_data("", org)
    dec = packer.decode_data(ddd)
    assert org == dec[0]


# EOF
