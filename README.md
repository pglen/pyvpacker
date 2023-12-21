
# pypacker

##    Encode / Decode arbitrary data into a string.

    Op Codes (type codes):

    Int Number            i
    Float Number          f
    Character             c
    String                s
    Binary                b

    List                  a         (array) gets encoded as extended
    Tuple                 t         gets encoded as extended (x)
    Dict                  d         gets encoded as extended (x)

    Extended              x         encoded as new packer string (recursive)

    Usage:

        arr_of_data = [datax, [ datay], { dataz : valz } ... etc]
        formatstr = ""
        pb  = packbin()
        newdata  = pb.encode_data(formatstr, arr_of_data)
        decdata  = pb.decode_data(newdata)
        ?assert?(decdata == arr_of_data)

    Empty format string will use the auto-detected types: (recommended)

        newdata  = pb.encode_data("", arr_of_data)

        Preserves type and data. It is (mostly) 7/8 bit clean on
    both python2 and python 3.

    Note: python2 'bytes' type is a place holder - avoid encoding bytes on python 2
    and decoding bytes on python 3; or at least be aware of the issues. This does
    not effect the decoded data, but it does effect the cypher text.

      The following comes into play when one encodes data with python 2 and
    decodes it in python 3.

          Python V2 and V3 str / bytes differences. In python 2 the 'bytes' type is
        an alias to the str type. It accommodates the whole palette of numbers in
        py2; thus we detect binary by looking at the str and seeing if non printable
        characters are present.  (the character < ' ' or > 'del')
        This works well, however we consider it a work-around; so please be aware.

       If you assure both encoder and decoder are the same python version, this
    issue does not exist.

   History:

    Sat 18.Feb.2023 decode binary after done decomposing it
    Mon 18.Dec.2023 moved to pypacker dir
    Tue 19.Dec.2023 test for python2 python 3 -- note: bytes / v2 v3 differences
    Thu 21.Dec.2023 cleanmup, docs, etc ...

Pytest results:

    ============================= test session starts ==============================
    platform linux -- Python 3.10.12, pytest-7.4.3, pluggy-1.0.0
    rootdir: /home/peterglen/pgpygtk/pypacker/tests
    collected 20 items

    test_arr.py ..                                                           [ 10%]
    test_bin.py ..                                                           [ 20%]
    test_complex.py ..                                                       [ 30%]
    test_dict.py .                                                           [ 35%]
    test_float.py ..                                                         [ 45%]
    test_int.py ..                                                           [ 55%]
    test_packer.py ......                                                    [ 85%]
    test_str.py ...                                                          [100%]

    ============================== 20 passed in 0.09s ==============================
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.18, pytest-4.6.11, py-1.11.0, pluggy-0.13.1
    rootdir: /home/peterglen/pgpygtk/pypacker/tests
    collected 20 items

    test_arr.py ..                                                           [ 10%]
    test_bin.py ..                                                           [ 20%]
    test_complex.py ..                                                       [ 30%]
    test_dict.py .                                                           [ 35%]
    test_float.py ..                                                         [ 45%]
    test_int.py ..                                                           [ 55%]
    test_packer.py ......                                                    [ 85%]
    test_str.py ...                                                          [100%]

    ========================== 20 passed in 0.12 seconds ===========================


   # EOF
