__author__ = 'brendan'
# Adapted from http://programeveryday.com/post/implementing-a-basic-vigenere-cipher-in-python/
# Written by Dan Sackett on January 19, 2015
from itertools import cycle
import string


def encrypt(key, plaintext):
    """Encrypt the string and return the ciphertext"""
    pairs = zip(plaintext, cycle(key))
    result = ''

    for pair in pairs:
        total = reduce(lambda x, y: string.ascii_uppercase.index(x) + string.ascii_uppercase.index(y), pair)
        result += string.ascii_uppercase[total % 26]

    return result.lower()


def decrypt(key, ciphertext):
    """Decrypt the string and return the plaintext"""
    pairs = zip(ciphertext, cycle(key))
    result = ''

    for pair in pairs:
        print pair
        total = reduce(lambda x, y: string.ascii_uppercase.index(x) - string.ascii_uppercase.index(y), pair)
        result += string.ascii_uppercase[total % 26]

    return result
