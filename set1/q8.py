from helper import unhex
from q3 import score


# read each line and unhexlify and remove newline
with open("q8.data") as f:
    r = [unhex(i.strip()) for i in f.readlines()]

# given keysize
k = 16

# for each line
for id, l in enumerate(r):
    # split into blocks of size k
    blocks = [l[i : i + k] for i in range(0, len(l), k)]
    # for each block see if the block repeats in the line
    for b in blocks:
        if blocks.count(b) > 1:
            # offset because computers start at 0
            print(id + 1)
            break
