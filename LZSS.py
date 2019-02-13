import math
import bitarray


def encoder(minimum_match, window_size, buffer_size, input_file):
    # verifies that the parameters provided have correct types
    if not isinstance(minimum_match, int):
        raise TypeError("minimum_match must be of type 'int'")
    if not isinstance(window_size, int):
        raise TypeError("window_size must be of type 'int'")
    if not isinstance(buffer_size, int):
        raise TypeError("buffer_size must be of type 'int'")
    if not isinstance(input_file, bytes):
        raise TypeError("input_file must be of type 'bytes'")

    # determines the number of bits required to encode a pointer and a reference
    pointer_size = math.ceil(math.log2(window_size))
    reference_size = math.ceil(math.log2(max(buffer_size - minimum_match, 0) + 1))

    # initialise the cursor to position 0 (first character) and the size of the window to 0
    coding_position = 0
    window_index = 0
    input_length = len(input_file)
    encoded_string = ''

    # while the cursor position is still within the byte string, continue encoding
    while coding_position < input_length:
        buffer_index = 0
        last_occurrence = -1
        buffer_string = b''

        # Append bytes from the lookahead buffer to the character in the coding position until this sequence of
        # bytes does not appear in the sliding window.
        while coding_position + buffer_index < input_length and buffer_index <= buffer_size:
            buffer_string = input_file[coding_position: coding_position + buffer_index + 1]
            new_last_occurrence = input_file.rfind(buffer_string, coding_position - window_index, coding_position)
            if new_last_occurrence == -1:
                break
            last_occurrence = new_last_occurrence
            buffer_index += 1

        # encode as a double or a triple depending on the length of the match
        if buffer_index < minimum_match:
            buffer_index = 0
            next_char = buffer_string[0].to_bytes(length=1, byteorder="big")
            encoded_string += '1'+bin(ord(next_char))[2:].zfill(8)
        else:
            encoded_string += '0' + bin((coding_position - last_occurrence))[2:].zfill(pointer_size)
            encoded_string += bin(buffer_index)[2:].zfill(reference_size)
            buffer_index -= 1
        coding_position += buffer_index + 1
        window_index = min(window_size, coding_position)
    return bitarray.bitarray(encoded_string, endian="big")


def decoder(minimum_match, window_size, buffer_size, input_bit_array):
    # verifies that the parameters have been given the correct type
    if not isinstance(minimum_match, int):
        raise TypeError("minimum_match must be of type 'int'")
    if not isinstance(window_size, int):
        raise TypeError("window_size must be of type 'int'")
    if not isinstance(buffer_size, int):
        raise TypeError("buffer_size must be of type 'int'")
    try:
        input_bit_array.to01()
    except Exception:
        raise TypeError("input_bit_array must be of type 'bitarray'")

    # initialise the decoded string as an empty byte string
    # set the current position in the input bit array (s_length) to 0
    input_length = len(input_bit_array)
    decoded_string = b''
    decoded_string_length = 0
    s_length = 0

    # calculates the pointer size (p_size) and reference size (r_size) that were used to encode
    p_size = math.ceil(math.log2(window_size))
    r_size = math.ceil(math.log2(max(buffer_size - minimum_match, 0) + 1))

    # while the current position in the input bit array is less than the total length of the input, continue decoding
    while s_length < input_length:
        # get the bit flag (0 or 1) and move the current position along 1
        bit_flag = int(input_bit_array[s_length: s_length + 1].to01(), 2)
        s_length += 1

        # if the bit flag is a 1, decode as a double, otherwise decode as a triple
        if bit_flag == 1:
            decoded_string += input_bit_array[s_length: s_length + 8].tobytes()
            s_length += 8
            decoded_string_length += 1

        elif bit_flag == 0:
            pointer = int(input_bit_array[s_length: s_length + p_size].to01(), 2)
            reference_length = int(input_bit_array[s_length + p_size: s_length + p_size + r_size].to01(), 2)
            last_occurrence = decoded_string_length - pointer
            decoded_string += decoded_string[last_occurrence:last_occurrence+reference_length]
            decoded_string_length += reference_length
            s_length += p_size + r_size
    return decoded_string
