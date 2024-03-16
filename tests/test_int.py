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
org =  1234

def test_int(capsys):

    ddd = packer.encode_data("", org)
    print(ddd)
    captured = capsys.readouterr()

    out = "pg s1 'i' i4 1234 \n"
    assert captured.out == out

def test_enc_dec(capsys):

    ddd = packer.encode_data("", org)
    dec = packer.decode_data(ddd)
    assert org == dec[0]


# EOF
