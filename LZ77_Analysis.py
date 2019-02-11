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

print(type(myfile))


encoded_version = encoder(500, 500, myfile)
print(encoded_version.decode('ascii'))

