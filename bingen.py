import sys

org2 = b""
for aa in range(5, 15):
    org2 += str(aa).encode("utf-8")

    #if sys.version_info[0] > 2:
    #    org2 += bytes(chr(aa), "utf-8")
    #else:
    #    org2 += bytearray(chr(aa))

print(org2)