from LZ77 import encoder, decoder
import bitarray

# string = 'string'
# encoded_string = string.encode('ascii')
# for l in encoded_string:
#     print(l)
# print(type(encoded_string))
# print(encoded_string.decode())

with open('Input/greymickey.bmp', 'rb') as file:
    myfile = file.read()
    window = len(myfile)
    print(len(myfile))
    ba = bitarray.bitarray(endian="little")
    ba.frombytes(myfile)
    print(ba.length())
    encoded_version = encoder(window, window, myfile)
    len(encoded_version)
    print('encoded length '+str(len(encoded_version)))
    decoded_version = decoder(window, window, encoded_version)


    #turn image files back to files??


