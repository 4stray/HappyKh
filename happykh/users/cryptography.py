from Crypto.Cipher import DES
from happykh.settings import ENCODING_DES_KEY


def pad(text):
    while len(text) % 8 != 0:
        text += b' '
    return text


def encode(encoding_text):
    """

    :param encoding_text: String
    :return:
    """
    des = DES.new(ENCODING_DES_KEY.encode(), DES.MODE_ECB)

    padded_text = pad(encoding_text.encode())
    encoded_text = des.encrypt(padded_text)
    hex_representation = encoded_text.hex()

    return hex_representation


def decode(decoding_hex):
    """

    :param decoding_hex:
    :return:
    """
    des = DES.new(ENCODING_DES_KEY.encode(), DES.MODE_ECB)

    decoding_bytes = bytes.fromhex(decoding_hex)
    decoded_bytes = des.decrypt(decoding_bytes)
    decoded_text = decoded_bytes.decode()
    cleared_text = str(decoded_text).replace(" ", "")

    return cleared_text
