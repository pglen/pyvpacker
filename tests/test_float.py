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
org =  1234.1234

def test_float(capsys):

    ddd = packer.encode_data("", org)
    print(ddd)
    captured = capsys.readouterr()

    out = "pg s1 'f' f8 1234.123400 \n"
    assert captured.out == out

def test_enc_dec(capsys):

    ddd = packer.encode_data("", org)
    dec = packer.decode_data(ddd)
    assert org == dec[0]

# EOF
