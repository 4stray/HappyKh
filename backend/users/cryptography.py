"""Functions for encoding and decoding data in users app"""
from Crypto.Cipher import DES
from happykh.settings import ENCODING_DES_KEY


def encode(encoding_text):
    """
    Encodes str value into bytes using DES, returns it's hex representation
    :param encoding_text: String
    :return:
    """
    des = DES.new(ENCODING_DES_KEY.encode(), DES.MODE_ECB)

    while (len(encoding_text) % 8) != 0:
        encoding_text += " "
    encoded_text = des.encrypt(encoding_text.encode())
    hex_representation = encoded_text.hex()

    return hex_representation


def decode(decoding_hex):
    """
    Decodes bytes' hex representation into string using DES
    :param decoding_hex: String
    :return: String
    """
    des = DES.new(ENCODING_DES_KEY.encode(), DES.MODE_ECB)

    decoding_bytes = bytes.fromhex(decoding_hex)
    decoded_bytes = des.decrypt(decoding_bytes)
    decoded_text = decoded_bytes.decode()
    cleared_text = str(decoded_text).rstrip()

    return cleared_text
