#!/usr/bin/env python

from __future__ import print_function

import os, sys, getopt, signal, select, string, time
import struct, stat, base64, random, zlib

#__all__ = [ packbin, ]

__doc__ =   \
'''
    Encode / Decode arbitrary data in a string. Preserves type and data.
    It is 8 bit clean on both python[2|3]

    Op Codes (type codes):

        Int Number            i
        Float Number          f
        Character             c
        String                s
        Binary                b

        List                  a     (array) gets encoded as extended
        Tuple                 t     gets encoded as extended (x)
        Dict                  d     gets encoded as extended (x)

        Extended              x     encoded as new packer string (recursive)

    Usage:

        pb  = packbin()
        newdata  = pb.encode_data(formatstr, arr_of_data)
        decdata  = pb.decode_data(newdata)
        ?assert?(decdata == arr_of_data)

    Empty format string will use auto detected types

        newdata  = pb.encode_data("", arr_of_data)

      The following comes into play when one encodes data with python 2 and
    decodes in python 3.

      Python V2 and V3 str / bytes differences. In python 2 the 'bytes' type is
    an alias to the str type. It accomodates the whole palet of numbers in
    py2; thus we detect binary by looking at the str and seeing if non printable
    characters are present.   < ' ' or > 'del'. This works well, however we consider
    this a workaround; so please be aware. If unsure, use the same py versin on
    both encode / decode. If that is difficult to assure, use py 3.x on both.

   History:

    Sat 18.Feb.2023 decode binary after done decomposing it
    Mon 18.Dec.2023 moved to pypacker dir
    Tue 19.Dec.2023 test for python2 python 3 -- note: bytes / v2 v3 differences
    Sun 04.Feb.2024 optimized. str += replaced with join
    Sun 04.Feb.2024 optimized ... scan is done on partial / look ahead basis
    Thu 15.Feb.2024 published to pip

'''

version = "1.0"

# ------------------------------------------------------------------------

class packbin():

    class InvalidType(Exception):

        def _init_(self, message):
             self.message = message

        def _str_(self):
            return(self.message)

    def __init__(self):

        self.pgdebug = 0
        self.dec_binary = True

        # -----------------------------------------------------------------------
        # This array of functions will call the appropriate function
        # Note the p' and 'g' are not in this type list, they denote
        # extended list

        self.typeact = [
                 ["i", self._got_int, self._found_int],
                 ["l", self._got_long, self._found_long],
                 ["f", self._got_float, self._found_float],
                 ["c", self._got_char, self._found_char],
                 ["s", self._got_str, self._found_str],
                 ["b", self._got_bin, self._found_bin],
                 ["a", self._got_list, self._found_list],
                 ["t", self._got_tuple, self._found_tuple],
                 ["x", self._got_xtend, self._found_ext],
                 ["d", self._got_dict, self._found_dict],
                ]

        self.verbose = 0

    # These functions contain the ations on encode

    def _got_int(self, tt, var):
        #print ("got int", var)
        return "%c%d %d " %  (tt, 4, var)

    def _got_long(self, tt, var):
        #print ("got long", var)
        return "%c%d %d " %  (tt, 8, var)

    def _got_float(self, tt, var):
        #print ("got num", "'" + str(var) + "'")
        return "%c%d %f " %  (tt, 8, var)

    def _got_char(self, tt, var):
        #print ("got char", "'" + str(var) + "'")
        return "%c%d %c " %  (tt, 1, var)

    def _got_str(self, tt, var):
        #print ("got str", "'" + var + "'")
        return "%c%d '%s' " %  (tt, len(var), var)

    def _got_bin(self, tt, var):

        #print("tt", tt, "var", var)
        #print("var", type(var))
        if type(var) == str:
            #var = bytes(var, 'utf-8')
            var = bytes(var)

        enco    = base64.b64encode(var)
        if sys.version_info[0] > 2:
            enco  = enco.decode()
            #enco  = enco.decode("utf-8")

        #print ("got bin", "'" + enco + "'")
        return "%c%d '%s' " %  (tt, len(enco), enco)

    def _got_list(self, tt, var):
        #print ("got list", "'" + str(var) + "'")
        enco = self.encode_data("", *var)
        return "%c%d '%s' " %  (tt, len(enco), enco)

    def _got_tuple(self, tt, var):
        #print ("got tuple", "'" + str(var) + "'")
        enco = self.encode_data("", *var)
        return "%c%d '%s' " %  (tt, len(enco), enco)

    def _got_xtend(self, tt, var):
        #print ("got xtend", "'" + str(var) + "'")
        return "%c%d [%s] " %  (tt, len(var), var)

    def _got_dict(self, tt, var):
        #print ("got dict", "'" + str(var) + "'")
        # Flatten it
        ccc = []
        for aa in var:
            ccc.append((aa, var[aa]))
        sss = self.encode_data("", ccc)
        return "%c%d '%s' " %  (tt, len(sss), sss)

    def _reclen(self, xstr):

        idxx = 0
        #print ("found:", xstr[:32], end=' ')
        idxx = 1
        nnn = xstr[idxx:].find(" ")
        if nnn < 0:
            print("bad xencoding at ", xstr[:idxx+12])

        slen = int(xstr[idxx:idxx+nnn])
        #print("slen", slen)

        #if slen >= len(xstr):
        #    print("err bad xencoding at ", xstr[:idxx+12])

        idxx += nnn + 2
        #print(slen)
        return slen

    # ------------------------------------------------------------------------
    # Return var and consumed number of characters

    def _found_char(self, xstr):
        idxx = 0; var = 0
        #print ("found int:", xstr)
        if xstr[1:3] != "1 ":
            print("bad encoding at ", xstr[idxx:idxx+5])
            raise(ValueError("Bad encoding at char '%s'" % xstr[idxx:idxx+5]))
            return idxx, var

        idxx = 3
        nnn = xstr[idxx:].find(" ")
        if nnn < 0:
            print("bad encoding at ", xstr[idxx:idxx+5])
            return idxx, var

        var = ord(xstr[idxx:idxx+nnn])
        #print("char:", "'" + chr(var) + "'")
        idxx += nnn + 1;
        #print("int idxx:", idxx, "var:", var, "next:", "'" + xstr[idxx:idxx+6] + "'")
        return idxx, chr(var)

    def _found_int(self, xstr):
        idxx = 0; var = 0
        #print ("found int:", xstr)
        if xstr[1:3] != "4 ":
            print("bad encoding at ", xstr[idxx:idxx+5])
        idxx = 3
        nnn = xstr[idxx:].find(" ")
        if nnn < 0:
            print("bad encoding at ", xstr[idxx:idxx+5])
        var = int(xstr[idxx:idxx+nnn])
        #print("int:", var)
        idxx += nnn + 1;
        #print("int idxx:", idxx, "var:", var, "next:", "'" + xstr[idxx:idxx+6] + "'")
        return idxx, var

    def _found_long(self, xstr):
        idxx = 0; var = 0
        #print ("found long:", xstr)
        if xstr[1:3] != "8 ":
            print("bad encoding at ", xstr[idxx:idxx+5])
        idxx = 3
        nnn = xstr[idxx:].find(" ")
        if nnn < 0:
            print("bad encoding at ", xstr[idxx:idxx+5])
        var = int(xstr[idxx:idxx+nnn])
        #print("long:", var)
        idxx += nnn + 1;
        #print("long idxx:", idxx, "var:", var, "next:", "'" + xstr[idxx:idxx+6] + "'")
        return idxx, var

    def _found_float(self, xstr):
        idxx = 0; var = 0
        #print ("found long:", xstr)
        if xstr[1:3] != "8 ":
            print("bad encoding at ", xstr[idxx:idxx+5])
        idxx = 3
        nnn = xstr[idxx:].find(" ")
        if nnn < 0:
            print("bad encoding at ", xstr[idxx:idxx+5])
        var = float(xstr[idxx:idxx+nnn])
        #print("float:", var)
        idxx += nnn + 1;
        #print("float idxx:", idxx, "var:", var, "next:", "'" + xstr[idxx:idxx+6] + "'")
        return idxx, var

    def _found_str(self, xstr):
        idxx = 0
        #print ("found str:", xstr)
        idxx = 1
        nnn = xstr[idxx:].find(" ")
        if nnn < 0:
            print("bad encoding at ", xstr[idxx:idxx+5])
        #print ("found num:", xstr[idxx:idxx+nnn])
        slen = int(xstr[idxx:idxx+nnn])
        #print("slen", slen)
        if slen >= len(xstr):
            print("bad encoding at ", xstr[idxx:idxx+5])
        idxx += nnn + 2
        sval = xstr[idxx:idxx+slen]
        #print("str:", "'" + sval + "'")
        idxx += slen + 2
        #print("idxx:", idxx, "var:", "{" + sval + "}", "next:", "'" + xstr[idxx:idxx+6] + "'")
        return idxx, sval

    def _found_dict(self, xstr):
        idxx =  0
        #print ("found dict:", xstr)
        idxx =  1
        nnn = xstr[idxx:].find(" ")
        if nnn < 0:
            print("bad encoding at ", xstr[idxx:idxx+5])
        slen = int(xstr[idxx:idxx+nnn])
        #print("slen=", slen)
        if slen >= len(xstr):
            print("bad encoding at ", xstr[idxx:idxx+5])
        idxx += nnn + 2
        sval = str(xstr[idxx:idxx+slen])
        #print("dict str:", "'" + sval + "'")
        # iterate dict str
        deco = self.decode_data(sval)
        idxx += slen + 2
        #print("idxx:", idxx, "var:", "{" + sval + "}", "next:", "'" + xstr[idxx:idxx+6] + "'")
        ddd = {}
        for aaa in deco[0]:
            #print("aaa", aaa)
            ddd[aaa[0]] = aaa[1]
        return idxx, ddd

    def _found_ext(self, xstr):
        idxx = 0
        #print ("found ext:", xstr)
        idxx = 1
        nnn = xstr[idxx:].find(" ")
        if nnn < 0:
            print("bad encoding at ", xstr[idxx:idxx+5])
        slen = int(xstr[idxx:idxx+nnn])
        #print("slen", slen)
        if slen >= len(xstr):
            print("bad encoding at ", xstr[idxx:idxx+5])
        idxx += nnn + 2
        sval = xstr[idxx:idxx+slen]
        #print("ext:", "'" + sval + "'")
        idxx += slen + 2
        #print("idxx:", idxx, "var:", "{" + sval + "}", "next:", "'" + xstr[idxx:idxx+6] + "'")
        return idxx, sval

    def _found_bin(self, xstr):
        idxx = 0
        #print ("found bin:", xstr)
        idxx = 1
        nnn = xstr[idxx:].find(" ")
        if nnn < 0:
            print("bad encoding at ", xstr[idxx:idxx+5])
        slen = int(xstr[idxx:idxx+nnn])
        #print("slen", slen)
        if slen >= len(xstr):
            print("bad encoding at ", xstr[idxx:idxx+5])
        idxx += nnn + 2
        sval = str(xstr[idxx:idxx+slen])
        #print("bin:",  sval )
        deco   = base64.b64decode(sval)

        #if self.dec_binary:
        #    deco2 = deco.decode('utf-8')
        #else:
        #    deco2 = deco

        #print("deco", type(deco), deco) #, type(deco2), deco2)

        idxx += slen + 2
        #print("idxx:", idxx, "var:", "{" + sval + "}", "next:", "'" + xstr[idxx:idxx+6] + "'")
        return idxx, deco

    def _found_list(self, xstr):
        idxx = 0
        #print ("found list:", xstr)
        idxx = 1
        nnn = xstr[idxx:].find(" ")
        if nnn < 0:
            print("bad encoding at ", xstr[idxx:idxx+5])
        slen = int(xstr[idxx:idxx+nnn])
        #print("slen", slen)
        if slen >= len(xstr):
            print("bad encoding at ", xstr[idxx:idxx+5])
        idxx += nnn + 2
        sval = str(xstr[idxx:idxx+slen])
        deco = self.decode_data(sval)
        idxx += slen + 2
        #print("idxx:", idxx, "var:", "{" + sval + "}", "next:", "'" + xstr[idxx:idxx+6] + "'")
        return idxx, deco

    def _found_tuple(self, xstr):
        idxx = 0
        #print ("found tuple:", xstr)
        idxx = 1
        nnn = xstr[idxx:].find(" ")
        if nnn < 0:
            print("bad encoding at ", xstr[idxx:idxx+5])
        slen = int(xstr[idxx:idxx+nnn])
        #print("slen", slen)
        if slen >= len(xstr):
            print("bad encoding at ", xstr[idxx:idxx+5])
        idxx += nnn + 2
        sval = str(xstr[idxx:idxx+slen])
        deco = self.decode_data(sval)
        idxx += slen + 2
        #print("idxx:", idxx, "var:", "{" + sval + "}", "next:", "'" + xstr[idxx:idxx+6] + "'")
        return idxx, tuple(deco)

    def _eval_one(self, dstr, idx2):
        #print ("  eval_one", dstr[idx2:])
        nstr = dstr[idx2:idx2+1]
        #print("nstr: ", "[" + nstr + "]")
        found = False; idx3 = 1; val = None
        for cc in self.typeact:
            if cc[0] == nstr:
                #print ("found", cc[0], cc[1], formstr[idx])
                # optizer: we pass expected length to slice. note the 16
                # is we added length for the expected format characters
                if cc[2]:
                    rlen = self._reclen(dstr[idx2:idx2+16])
                    #print (rlen, dstr[idx2:idx2+64])
                    idx3, val = cc[2](dstr[idx2:idx2+rlen+16])
                found = True
        if not found:
            # xxx We do not raise an exception, rather inform the user
            #print("Warn: Invalid char in '%c' (at %d) format string in '%s" % (nstr, idx2, dstr))
            if self.verbose:
                print("Warn: Invalid char in '%c'" % nstr)
            # We raise an exception (by pop demand)
            #raise self.InvalidType("Invalid type descriptor",  nstr, "at offset: %d" % idx2)

        return idx3, val

    # Estabilish a proper format string autmatically
    def autotype(self, xdata):

        aaa = ""
        for aa in xdata:

            if self.pgdebug > 5:
                print("typename:", type(aa).__name__)

            if type(aa).__name__ == "int":
                #print (aa)
                aaa += "i"

            elif type(aa).__name__ == "long":
                #print (aa)
                aaa += "l"

            elif type(aa).__name__ == "str":
                #print(crysupp.hexdump(aa, len(aa)))
                bbb = False
                # see if binary, only on PY two
                if sys.version_info[0] < 3:
                    for bb in aa:
                        if ord(bb) > 126 or ord(bb) < ord(' '):
                            bbb = True
                            break
                if bbb:
                    aaa += "b"
                else:
                    if len(aa) == 1:
                        aaa += "c"
                    else:
                        aaa += "s"

            # Py 2 does not have this ... safe to test in both
            elif type(aa).__name__ == "bytes":
                #print(crysupp.hexdump(aa, len(aa)))
                aaa += "b"

            elif type(aa).__name__ == "float":
                #print (aa)
                aaa += "f"
            elif type(aa).__name__ == "list":
                #print ("adding list")
                aaa += "a"

            elif type(aa).__name__ == "tuple":
                #print ("adding tuple")
                aaa += "t"

            elif type(aa).__name__ == "dict":
                #print ("adding dict")
                aaa += "d"

            else:
                raise self.InvalidType( "Unsupported type: "  + str(type(aa).__name__ ))

        if self.pgdebug > 3:
            print("autotype res", aaa)

        return aaa

    # Add front string

    def _encode_data(self, front, *formstr):

        #print("front", front, "formstr", formstr)

        #ttt = time.time()

        localf = formstr[0]
        if  localf == "":
            localf = self.autotype(formstr[1:])
            if self.verbose > 6:
                print("Autotype: '" + localf + "'");
        else:
            if self.verbose > 6:
                print("formatstr:", formstr[0])
                for aa in formstr:
                    print("got format:", aa)

        packed_arr = []
        #packed_str = front
        packed_arr.append(front)

        # Add the form string itself
        #packed_str += self._got_str("s", localf)
        packed_arr.append(self._got_str("s", localf))

        idx = 1;
        for bb in localf:
            found = 0
            #print("encoding item: ", type(formstr[idx]) )
            #print("bb", bb, end=" ")
            for cc in self.typeact:
                if cc[0] == bb:
                    if self.verbose > 5:
                        print ("found", cc[0], cc[1], formstr[idx])
                    if cc[1]:
                        #packed_str += cc[1](bb, formstr[idx])
                        packed_arr.append (cc[1](bb, formstr[idx]))
                    idx += 1
                    found = True
            if not found:
                raise ValueError("Invalid char in '%c' format string" % bb)

        if idx < len(formstr):
            raise ValueError("More data than chars in format string")

        #print ("ttt=%.2f ns" % (1000000 *(time.time() - ttt)))
        #ttt = time.time()
        packed_str = "".join(packed_arr)
        #print ("ttt2=%.2f ns" % (1000000 *(time.time() - ttt)))
        return packed_str


    def _decode_data(self, dstr):

        #print ("---org:\n", dstr, "org---")

        if type(dstr) != str:
            try:
                dstr = dstr.decode('utf-8')
            except:
                dstr = dstr.decode('cp437')

        if dstr[0:3] != 'pg ':
            raise ValueError("Cannot decode, must begin with pg sequence.")
            #print("pypacker decode: Error, must begin with 'pg '")
            #return ""

        idx = 3
        if dstr[idx] != 's':
            raise ValueError("pypacker decode: Error, must have format string at the beginning.")
            #return ""
        idx += 1

        nnn = dstr[idx:].find(" ")

        #print("nnn", nnn)
        #print("lens", "'" + dstr[idx:idx+nnn] + "'")

        flen = int(dstr[idx:idx+nnn])
        if flen > len(dstr) - idx:
            raise ValueError("pypacker decode: Error, bad decode: (overflow) at %d", idx)

        #print("flen", flen)

        idx += nnn + 1
        fstr = dstr[idx:idx+flen+2]
        #print("fstr: ", "[" + fstr + "]")
        idx += flen + 3;

        #print("start", "[" + dstr[idx:] + "]")

        try:
            arr = []
            while True:
                if idx >= len(dstr):
                    break
                #ttt = time.time()
                idx2, val = self._eval_one(dstr, idx)
                #print("idx:", idx, "val:", dstr[idx:idx+24], "idx2", idx2)
                #print ("ttt=%.2f ns" % (1000000 *(time.time() - ttt)))

                idx += idx2
                arr.append(val)
        except:
            #print("Exception at:", idx, "val:", val)
            raise

        if self.pgdebug > 1:
           print("output:", arr)

        return arr

    ##########################################################################
    # Encode data into a string
    # Pass format string as the first element. Empty string switches on
    # autotype

    def encode_data(self, *formstr):

        #print("type", type(formstr[1]), len(formstr[1]))
        #if type(formstr[1]).__name__ == "NoneType":
        #    raise ValueError("Cannot encode, must be an iterable")

        if self.pgdebug:
           print("encode input:", *formstr)
        rrr = self._encode_data("pg ", *formstr)
        if self.pgdebug > 1:
           print("encode output:", rrr)

        return rrr

    def decode_data(self, dstr):

        #print ("---org:\n", dstr, "org---")
        if self.pgdebug:
            print ("decode input", dstr)
        rrr = self._decode_data(dstr)
        if self.pgdebug > 1:
           print("decoded output:", rrr)

        return rrr

if __name__ == '__main__':
    print("This file was meant to run as a module")

# EOF