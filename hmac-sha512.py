#!usr/bin/python

import hmac, hashlib

def hammingDistance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(bool(ord(ch1) - ord(ch2)) for ch1, ch2 in zip(s1,s2))

def main():
    Key = ""
    Input = ""
    while True:
        Key = input( "Introduzca la clave que quiere utilizar para realizar las pruebas\n" )
        Input = input( "Introduzca el mensaje que quiere utilizar para realizar las pruebas\n" )
        Key = str.encode( Key )
        Input = str.encode( Input )
        sign = hmac.new( Key, Input, hashlib.sha512).hexdigest()
        Key = Key.decode("utf-8")
        Input = Input.decode("utf-8")
        print ( 'HMAC-SHA512 generada con \'{0}\' y \'{1}\': {2}\n'.format(Key, Input, sign) )


if __name__ == '__main__':
    main()
