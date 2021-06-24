def validiate_pkcs7(data: bytes):
    last_item = data[-1]
    if data[-last_item:] == bytes([last_item] * last_item):
        return True
    raise ValueError("Bad padding")


def unpad_pkcs7(data: bytes):
    if validiate_pkcs7(data):
        return data[: -data[-1]]


if __name__ == "__main__":
    print(unpad_pkcs7(b"ICE ICE BABY\x04\x04\x04\x04"))
    # print(unpad_pkcs7(b"ICE ICE BABY\x05\x05\x05\x05"))
    # print(unpad_pkcs7(b"ICE ICE BABY\x01\x02\x03\x04"))
