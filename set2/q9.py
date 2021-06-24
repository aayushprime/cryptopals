def pad_pkcs7(data, blocksize):
    filler_character_size = blocksize - len(data) % blocksize
    data += bytes([filler_character_size] * filler_character_size)
    return data


if __name__ == "__main__":
    print(pad_pkcs7(b"YELLOW SUMBARINE", 20))
