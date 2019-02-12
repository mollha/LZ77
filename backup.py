import math
import bitarray


def encoder(window_size, buffer_size, input_file):
    input_file = input_file.decode()
    print(input_file)
    pointer_size = math.ceil(math.log2(window_size + 1))
    reference_size = math.ceil(math.log2(buffer_size + 1))
    print('amount ' + str(pointer_size + reference_size + 8))

    # takes bitarray object as input
    # input file is in bytes

    # initialise the cursor to position 0 (first character) and the size of the window to 0
    coding_position = 0
    window_index = 0
    input_length = len(input_file)
    encoded_string = ''

    # while the cursor position is still within the string, continue encoding
    while coding_position < input_length:
        buffer_index = 0
        last_occurrence = -1
        buffer_string = ''

        # Append characters from the lookahead buffer to the character in the coding position until this sequence of
        # characters does not appear in the sliding window.
        while coding_position + buffer_index < input_length and buffer_index <= buffer_size:
            buffer_string += input_file[coding_position + buffer_index]
            # buffer_string.append(bytes(str(input_file[coding_position + buffer_index]).zfill(3), "ascii"))
            new_last_occurrence = input_file.decode().rfind(buffer_string, coding_position - window_index, coding_position)
            if new_last_occurrence == -1:
                break
            last_occurrence = new_last_occurrence
            buffer_index += 1

        # set the position of the last occurrence to the coding position so that they cancel to 0 later
        if last_occurrence == -1:
            last_occurrence = coding_position

        # sets the character that signifies EOF (end of file), otherwise finds the next character in the input
        if coding_position + buffer_index == input_length:
            next_char = '-'
        else:
            next_char = buffer_string[-1]

        # creates 3-tuple, increments the coding position and increases the window size if possible
        encoded_string += bin((coding_position - last_occurrence))[2:].zfill(pointer_size)
        encoded_string += bin(buffer_index)[2:].zfill(reference_size)
        # encoded_string += buffer_index.to_bytes(math.ceil(math.log2(buffer_size)), byteorder='big')
        encoded_string += bin(ord(next_char))[2:].zfill(8)
        coding_position += buffer_index + 1
        window_index = min(window_size, coding_position)
    return bitarray.bitarray(encoded_string, endian="big")


def decoder(window_size, buffer_size, input_bitarray):
    input_length = len(input_bitarray)
    decoded_string = b''
    decoded_string_length = 0

    pointer_size = math.ceil(math.log2(window_size + 1))
    reference_size = math.ceil(math.log2(buffer_size + 1))

    while decoded_string_length < input_length:

        print(input_bitarray[decoded_string_length : decoded_string_length + pointer_size].tostring())
        pointer = input_bitarray[decoded_string_length : decoded_string_length + pointer_size].tostring()


        decoded_string_length += pointer_size
        decoded_string += input_bitarray[decoded_string_length : decoded_string_length + reference_size].tobytes()
        decoded_string_length += reference_size
        decoded_string += input_bitarray[decoded_string_length: decoded_string_length + 8].tobytes()
        decoded_string_length += 8
    return decoded_string