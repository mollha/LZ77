import math
import bitarray


def encoder(window_size, buffer_size, input_file):
    pointer_size = math.ceil(math.log2(window_size + 1))
    reference_size = math.ceil(math.log2(buffer_size + 1))

    # takes bit array object as input
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
        buffer_string = b''

        # Append characters from the lookahead buffer to the character in the coding position until this sequence of
        # characters does not appear in the sliding window.
        while coding_position + buffer_index < input_length and buffer_index <= buffer_size:
            buffer_string = input_file[coding_position: coding_position + buffer_index + 1]
            new_last_occurrence = input_file.rfind(buffer_string, coding_position - window_index, coding_position)
            if new_last_occurrence == -1:
                break
            last_occurrence = new_last_occurrence
            buffer_index += 1

        # set the position of the last occurrence to the coding position so that they cancel to 0 later
        if last_occurrence == -1:
            next_char = buffer_string[-1].to_bytes(length=1, byteorder="big")
            encoded_string += '1'
            encoded_string += bin(ord(next_char))[2:].zfill(8)
        else:
            encoded_string += '0'
            encoded_string += bin((coding_position - last_occurrence))[2:].zfill(pointer_size)
            encoded_string += bin(buffer_index)[2:].zfill(reference_size)
            buffer_index -= 1

        coding_position += buffer_index + 1
        window_index = min(window_size, coding_position)
    return bitarray.bitarray(encoded_string, endian="big")


def decoder(window_size, buffer_size, input_bit_array):
    input_length = len(input_bit_array)
    decoded_string = b''
    decoded_string_length = 0
    s_length = 0

    p_size = math.ceil(math.log2(window_size + 1))
    r_size = math.ceil(math.log2(buffer_size + 1))

    while s_length < input_length:
        bit_flag = int(input_bit_array[s_length: s_length + 1].to01(), 2)
        if bit_flag == 0:
            decoded_string += input_bit_array[s_length + 1: s_length + 9].tobytes()
            s_length += 9
            decoded_string_length += 1
        elif bit_flag == 1:
            pointer = int(input_bit_array[s_length: s_length + p_size].to01(), 2)
            reference_length = int(input_bit_array[s_length + p_size: s_length + p_size + r_size].to01(), 2)
            last_occurrence = decoded_string_length - pointer
            decoded_string += decoded_string[last_occurrence:last_occurrence+reference_length]
            s_length += 1 + p_size + r_size
            decoded_string_length += reference_length + 1
    return decoded_string
