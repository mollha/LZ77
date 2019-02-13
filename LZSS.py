import math
import bitarray


def encoder(window_size, buffer_size, input_file):
    if not isinstance(window_size, int):
        raise TypeError("window_size must be of type 'int'")
    if not isinstance(buffer_size, int):
        raise TypeError("buffer_size must be of type 'int'")
    if not isinstance(input_file, bytes):
        raise TypeError("input_file must be of type 'bytes'")

    minimum_match = 2
    pointer_size = math.ceil(math.log2(window_size))
    reference_size = math.ceil(math.log2(max(buffer_size - minimum_match, 0) + 1))
    # takes bit array object as input
    # input file is in bytes
    print('p :'+str(pointer_size))
    print('r :' + str(reference_size))
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
            print('FLAG 1')
            encoded_string += '1'+bin(ord(next_char))[2:].zfill(8)
        else:
            print('FLAG 2')
            encoded_string += '0' + bin((coding_position - last_occurrence))[2:].zfill(pointer_size)
            encoded_string += bin(buffer_index)[2:].zfill(reference_size)
            buffer_index -= 1
        print('e :' + str(encoded_string))
        coding_position += buffer_index + 1
        window_index = min(window_size, coding_position)
    return bitarray.bitarray(encoded_string, endian="big")


def decoder(window_size, buffer_size, input_bit_array):
    if not isinstance(window_size, int):
        raise TypeError("window_size must be of type 'int'")
    if not isinstance(buffer_size, int):
        raise TypeError("buffer_size must be of type 'int'")
    try:
        input_bit_array.to01()
    except Exception:
        raise TypeError("input_bit_array must be of type 'bitarray'")

    input_length = len(input_bit_array)
    decoded_string = b''
    decoded_string_length = 0
    s_length = 0

    minimum_match = 2
    p_size = math.ceil(math.log2(window_size))
    r_size = math.ceil(math.log2(max(buffer_size - minimum_match, 0) + 1))

    while s_length < input_length:
        bit_flag = int(input_bit_array[s_length: s_length + 1].to01(), 2)
        s_length += 1
        print('bit_flag '+str(bit_flag))
        if bit_flag == 1:
            decoded_string += input_bit_array[s_length: s_length + 8].tobytes()
            s_length += 8
            decoded_string_length += 1
            print(decoded_string)
        elif bit_flag == 0:
            pointer = int(input_bit_array[s_length: s_length + p_size].to01(), 2)
            reference_length = int(input_bit_array[s_length + p_size: s_length + p_size + r_size].to01(), 2)

            last_occurrence = decoded_string_length - pointer
            print('last :'+str(last_occurrence))
            print('length: '+str(decoded_string_length))
            print('pointer :'+str(pointer))
            decoded_string += decoded_string[last_occurrence:last_occurrence+reference_length]
            print(decoded_string)

            decoded_string_length += reference_length
            s_length += p_size + r_size
    return decoded_string
