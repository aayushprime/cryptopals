from helper import *
import string
from q3 import break_fixed_single_xor, score


def break_fixed_single_byte_from_list(filename):
    with open(filename) as f:
        r = f.readlines()
    best = ""
    b_score = 0
    for a in r:
        possible_max = break_fixed_single_xor(unhex(a.strip()))
        new_score = score(possible_max.decode())
        if new_score > b_score:
            b_score = new_score
            best = possible_max
    return best


if __name__ == "__main__":
    print(break_fixed_single_byte_from_list("q4.data"))
