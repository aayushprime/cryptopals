from helper import *
from q3 import break_fixed_single_xor
import base64
import itertools
from q5 import repeating_key_xor


def hamming(b1, b2):
    """hamming distance is the number of different bits
    we take xor and count the number of ones in the bits
    """
    p = fixed_xor(b1, b2)
    return bin(int(hexlify(p), 16)).count("1")


def find_normalized_edit_distance(data, keysize):
    # find slices and store in blocks, only take first 4 of the slices
    blocks = [data[i : i + keysize] for i in range(0, len(data), keysize)][:4]
    # using itertools find all combinations of the slices of size 2
    pairs = list(itertools.combinations(blocks, 2))
    # find scores for every pair and divide by keysize, take only first 6
    scores = [hamming(p[0], p[1]) / keysize for p in pairs][:6]
    # return average of scores
    return sum(scores) / len(scores)


def break_repeating_key_xor(data, keysize):
    # fill the remaining bytes with b"0" so that the data size is even
    while len(data) % keysize != 0:
        data += b"0"

    # split into blocks of keysize for creating slices
    blocks = [data[i : i + keysize] for i in range(0, len(data), keysize)]

    # create slices from blocks, take 1st from each block, 2nd from each block,etc.
    slices = []
    for i in range(keysize):
        l = [d[i] for d in blocks]
        slices.append(bytes(l))

    # accumulate keys of each slice
    # break_fixed_single_xor returns the value of string rather than key,
    # so xor with s[0] to get the key
    key = [break_fixed_single_xor(s)[0] ^ s[0] for s in slices]
    # return key as bytes object
    return bytes(key)


if __name__ == "__main__":
    # read the data and decode base64 into bytes
    r = base64.b64decode(open("q6.data").read())
    # key is the size where the normalized edit distance is minimum
    key_size = min(range(2, 41), key=lambda k: find_normalized_edit_distance(r, k))
    # print(key_size)

    key = break_repeating_key_xor(r, key_size)
    # print(key)

    # xor with key to get the actual string
    print(repeating_key_xor(r, key))
