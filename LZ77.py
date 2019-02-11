import math

def encoder(window_size, buffer_size, input_file):
    # takes BYTES object as input
    # input file is in bytes

    # initialise the cursor to position 0 (first character) and the size of the window to 0
    coding_position = 0
    window_index = 0
    input_length = len(input_file)
    encoded_string = b''

    # while the cursor position is still within the string, continue encoding
    while coding_position < input_length:
        buffer_index = 0
        last_occurrence = -1
        buffer_string = b''

        # Append characters from the lookahead buffer to the character in the coding position until this sequence of
        # characters does not appear in the sliding window.
        while coding_position + buffer_index < input_length and buffer_index <= buffer_size:
            # buffer_string += input_file[coding_position + buffer_index].to_bytes(3, byteorder='big')
            buffer_string += bytes(str(input_file[coding_position + buffer_index]), "ascii")
            new_last_occurrence = input_file.rfind(buffer_string, coding_position - window_index, coding_position)
            if new_last_occurrence == -1:
                break
            last_occurrence = new_last_occurrence
            buffer_index += 1

        # set the position of the last occurrence to the coding position so that they cancel to 0 later
        if last_occurrence == -1:
            last_occurrence = coding_position

        # sets the character that signifies EOF (end of file), otherwise finds the next character in the input
        if coding_position + buffer_index == input_length:
            next_char = ''
        else:
            next_char = buffer_string[-1]

        # creates 3-tuple, increments the coding position and increases the window size if possible
        coding_position += buffer_index+1
        window_index = min(window_size, coding_position)
        print(encoded_string)
        encoded_string += bytes(str(coding_position-last_occurrence), "ascii")
        print(encoded_string)
        encoded_string += bytes(str(buffer_index), "ascii")
        # encoded_string += buffer_index.to_bytes(math.ceil(math.log2(buffer_size)), byteorder='big')
        print(encoded_string)
        encoded_string += bytes(str(next_char), "ascii")
        print(encoded_string)
    return encoded_string


def decoder(input_list):
    decoded_string = ''
    decoded_string_length = 0

    # iterate in order through the list of 3-tuples to rebuild the original data
    for three_tuple in input_list:
        # backtrack to the position of the last occurrence of the character sequence, stored at index 0 of the 3-tuple
        last_occurrence = decoded_string_length-three_tuple[0]

        # copy the appropriate amount of characters (signified by index 1 of the 3-tuple) and add them to current string
        # add the character that follows this sequence to the end of the string
        decoded_string += decoded_string[last_occurrence:last_occurrence+three_tuple[1]] + three_tuple[2]

        # increase the length of the string by the length of the copied sequence plus the extra character
        decoded_string_length += three_tuple[1] + 1
    return decoded_string