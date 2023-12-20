    Encode / Decode arbitrary data into a string. Preserves type and data.
    It is 8 bit clean on both python[2|3]

    Note: python2 bytes type is a place holder - do not encode bytes on python 2
    and decode bytes on python 3

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
    this a workaround; so please be aware.

   History:

    Sat 18.Feb.2023 decode binary after done decomposing it
    Mon 18.Dec.2023 moved to pypacker dir
    Tue 19.Dec.2023 test for python2 python 3 -- note: bytes / v2 v3 differences

