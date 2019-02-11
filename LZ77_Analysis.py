from LZ77 import encoder
import bitarray

# string = 'string'
# encoded_string = string.encode('ascii')
# for l in encoded_string:
#     print(l)
# print(type(encoded_string))
# print(encoded_string.decode())

with open('Input/short_example', 'rb') as file:
    myfile = file.read()
    print(len(myfile))
    ba = bitarray.bitarray(endian="little")
    ba.frombytes(myfile)
    print(ba.length())
    print(ba[0:8].tobytes())
    print(type(ba))

print(type(myfile))


encoded_version = encoder(500, 500, myfile)
len(encoded_version)
print(len(encoded_version))
print(len('abracdabra'))

