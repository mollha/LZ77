from LZ77 import encoder
import bitarray

# string = 'string'
# encoded_string = string.encode('ascii')
# for l in encoded_string:
#     print(l)
# print(type(encoded_string))
# print(encoded_string.decode())

with open('Input/long_example', 'rb') as file:
    myfile = file.read()
    print(len(myfile))
    ba = bitarray.bitarray(endian="little")
    ba.frombytes(myfile)
    print(ba.length())
    print(type(ba))

print(type(myfile))


encoded_version = encoder(193, 193, ba)
len(encoded_version)
print('encoded length '+str(len(encoded_version)))
print(len('abracdabra'))

