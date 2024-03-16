#!/usr/bin/env python3

import  os, sys, getopt, signal, select, socket, time, struct
import  random, stat, os.path, datetime, threading, warnings
import  string

import gettext
gettext.bindtextdomain('thisapp', './locale/')
gettext.textdomain('thisapp')
_ = gettext.gettext

#base = os.path.dirname(os.path.realpath(__file__))
#sys.path.append(os.path.join(base,  '../pyvpacker'))

import twincore, pyvpacker

packer = pyvpacker.packbin()
core = twincore.TwinCore("second.pydb")

# Read in file with foreign characters
with open("konnen_pinata.txt") as file:
    strx = file.read()

# This is a hybrid of many types

org = [1, 2, strx, 'piñata',
    "\u0627\u0644\u062a\u0635\u0645\u064a\u0645",
    "aa", ["bb", b"dd",]]

print("org:\n", org)
packed = packer.encode_data("", *org)
#print("packed:", packed)
unpacked = packer.decode_data(packed)
print("unpacked:\n", unpacked)
if unpacked == org:
    print("OK")
else:
    print ("ERROR")

#
#packed2 = bytes(packed, 'utf-8')
#print("packed bin:", packed2)
#
#unpacked2 = packer.decode_data(packed2)
#print("unpacked bin:", unpacked2)
#
#thiskey = "ThisKey"     # use this key for save / retrieve

# Send / Retrieve data from DB

#core.save_data(thiskey, packed)
#rec_arr = core.retrieve(thiskey, 1)[0]
#
## The data went through encoding to binary, decode
#data = rec_arr[1].decode("cp437")
#print ("rec_arr:", data)
#rec_arr_upacked = packer.decode_data(data)
#print ("rec_arr_upacked:", rec_arr_upacked)

# EOF

