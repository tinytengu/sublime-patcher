import json
import binascii


def read_patterns(filename: str) -> dict:
    """ Read HEX patterns info from file.

    :param filename: file path to read from
    :type filename: str

    :return: patterns info
    :rtype: dict
    """
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def has_patterns(source: bytes, patterns: list[str]) -> bool:
    """ Verify HEX patterns existence in bytes.

    :param source: source bytes
    :type source: bytes

    :param patterns: patterns list
    :type patterns: list

    :return: patterns existence status
    :rtype: bool
    """
    for pattern in patterns:
        binary = binascii.unhexlify(pattern)
        if binary not in source:
            return False
    return True


def write_patterns(source: bytes, patterns: dict[str, str]) -> bytes:
    """ Write patterns to bytes.

    :param source: source bytes
    :type source: bytes

    :param patterns: patterns dictionary. `{"original": "replace_with"}`
    :type patterns: dict

    :return: modified bytes
    :rtype: bytes
    """
    for k, v in patterns.items():
        k_bin = binascii.unhexlify(k)
        v_bin = binascii.unhexlify(v)
        source = source.replace(k_bin, v_bin)
    return source
