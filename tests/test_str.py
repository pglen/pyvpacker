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

longz = "12340-9540987sdkljsdfakjbsdfkbds[p]" \
        "[jfaskljhfsdkljfdskjlsadfdasd], dsadsdd"

def test_str(capsys):

    ddd = packer.encode_data("", longz)
    print(ddd)
    captured = capsys.readouterr()

    out = "pg s1 's' s74 '12340-9540987sdkljsdfakjbsdfkbds[p][jfaskljhfsdkljfdskjlsadfdasd], dsadsdd' \n"

    assert captured.out == out

def test_enc_dec(capsys):

    ddd = packer.encode_data("", longz)
    dec = packer.decode_data(ddd)
    assert longz == dec[0]

def test_longz(capsys):

    ddd = packer.encode_data("", longz)
    dec = packer.decode_data(ddd)
    assert longz == dec[0]

# EOF
