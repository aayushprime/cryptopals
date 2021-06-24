from Crypto.Cipher import AES
from set2.q9 import pad_pkcs7
from set2.q11 import gen_aes_key


def kv_parser(string: bytes):
    s = string.split(b"&")
    dictionary = {}
    for i in s:
        j = i.split(b"=")
        dictionary[j[0]] = j[1]
    return dictionary


def prune(string: bytes):
    return string.replace(b"&", b"").replace(b"=", b"")


def profile_for(email: bytes, id: bytes, role: bytes):
    data = {b"email": prune(email), b"uid": prune(id), b"role": prune(role)}
    return data


def encode(data):
    s = []
    for i in data:
        s.append(i + b"=" + data[i])
    return b"&".join(s)


def encrypt_aes(data: bytes, key: bytes) -> bytes:
    data = pad_pkcs7(data, 16)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)


def decrypt_aes(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data)


key = gen_aes_key()


def encrypt_profile(email, id, role):
    return encrypt_aes(encode(profile_for(email, id, role)), key)


def unpad_pkcs7(data: bytes):
    return data[: -data[-1]]


def decrypt_profile(data: bytes):
    return kv_parser(unpad_pkcs7(decrypt_aes(data, key)))


if __name__ == "__main__":
    # print(kv_parser(b"foo=bar&baz=qux&zap=zazzle"))
    # print(encode(profile_for(b"foo@bar.com", 99, b"user")))
    print(encrypt_profile(b"foo@bar.co&&==m", b"33", b"tes&&==tuser"))
    encrypted = encrypt_profile(b"foo@bar.com", b"33", b"testuser")
    decrypted = decrypt_profile(encrypted)
    print(decrypted)
