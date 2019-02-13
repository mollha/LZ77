from random import choice, randint
import string


def ab_string(length):
    bitstring = ''
    for bit in range(length):

        if randint(0, 1) == 0:
            bitstring += 'a'
        else:
            bitstring += 'b'
    return bitstring


def ascii_string(length):
    output = ''.join(choice(string.digits + string.punctuation + string.ascii_letters) for _ in range(length))
    return output
