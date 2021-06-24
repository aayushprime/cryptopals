from helper import *


def repeating_key_xor(data, key):
    xored = ""
    for i, d in enumerate(data):
        xored += chr(d ^ key[i % len(key)])
    return xored.encode()


if __name__ == "__main__":
    in_eng = """Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"""
    key = "ICE"

    print(hexlify(repeating_key_xor(in_eng.encode(), key.encode())))
    print(
        """0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"""
    )

    # print(hexlify(repeating_key_xor(in_eng2.encode(), key.encode())))
