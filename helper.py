#!/usr/bin/env python3

import base64
import binascii


def hexlify(l):
    return binascii.hexlify(l)


def unhex(l):
    return binascii.unhexlify(l)


def hex_string_to_base64(l):
    return base64.b64encode(unhex(l))


def fixed_xor(l1, l2):
    if len(l1) != len(l2):
        print("length not equal")
    l3 = ""
    for i, c in enumerate(l1):
        l3 += chr(c ^ l2[i])
    return l3.encode()
