import math
import bitarray


def encoder(window_size, buffer_size, input_file):
    # verifies that the parameters provided have correct types
    if not isinstance(window_size, int):
        raise TypeError("window_size must be of type 'int'")
    if not isinstance(buffer_size, int):
        raise TypeError("buffer_size must be of type 'int'")
    if not isinstance(input_file, bytes):
        raise TypeError("input_file must be of type 'bytes'")

    # determines the number of bits required to encode a pointer and a reference
    pointer_size = math.ceil(math.log2(window_size + 1))
    reference_size = math.ceil(math.log2(buffer_size + 1))

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

        # set the position of the last occurrence to the coding position so that they cancel to 0 later
        if last_occurrence == -1:
            last_occurrence = coding_position

        # sets the character that signifies EOF (end of file), otherwise finds the next byte in the input
        if coding_position + buffer_index == input_length:
            next_char = ' '
        else:
            next_char = buffer_string[-1].to_bytes(length=1, byteorder="big")

        # creates triple, increments the coding position and increases the window size if possible
        encoded_string += bin((coding_position - last_occurrence))[2:].zfill(pointer_size)
        encoded_string += bin(buffer_index)[2:].zfill(reference_size)
        encoded_string += bin(ord(next_char))[2:].zfill(8)
        coding_position += buffer_index + 1
        window_index = min(window_size, coding_position)
    return bitarray.bitarray(encoded_string, endian="big")


def decoder(window_size, buffer_size, input_bit_array):
    # verifies that the parameters have been given the correct type
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
    p_size = math.ceil(math.log2(window_size + 1))
    r_size = math.ceil(math.log2(buffer_size + 1))

    # while the current position in the input bit array is less than the total length of the input, continue decoding
    while s_length < input_length:
        # convert the chunk of bits into bytes (separate the triple into its constituents)
        pointer = int(input_bit_array[s_length: s_length + p_size].to01(), 2)
        reference_length = int(input_bit_array[s_length + p_size: s_length + p_size + r_size].to01(), 2)
        next_char = input_bit_array[s_length + p_size + r_size: s_length + p_size + r_size + 8].tobytes()

        # locate, copy and re-append the reference
        last_occurrence = decoded_string_length - pointer
        decoded_string += decoded_string[last_occurrence:last_occurrence+reference_length] + next_char

        # increase the length of the string by the number of bits added
        decoded_string_length += reference_length + 1
        s_length += 8 + p_size + r_size
    return decoded_string
