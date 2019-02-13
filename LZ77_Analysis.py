from LZSS import encoder, decoder
from generate import *
import time


# Analyses performance in all areas on a single input and takes average of 3 attempts for running times
def general_analysis(iterations, window_size, buffer_size, length):
    encoded_file = None
    min_decoder_time = None
    max_decoder_time = None
    min_encoder_time = None
    max_encoder_time = None
    total_encoder_time = 0
    total_decoder_time = 0

    for iteration in range(iterations):
        input_file = ab_string(length).encode()
        time_stamp1 = time.time() * 1000
        encoded_file = encoder(window_size, buffer_size, input_file)
        time_stamp2 = time.time() * 1000
        decoder(window_size, buffer_size, encoded_file)
        time_stamp3 = time.time() * 1000
        encoder_time = time_stamp2 - time_stamp1
        decoder_time = time_stamp3 - time_stamp2
        total_encoder_time += encoder_time
        total_decoder_time += decoder_time
        if min_encoder_time is None or encoder_time < min_encoder_time:
            min_encoder_time = round(encoder_time, 3)
        if max_encoder_time is None or encoder_time > max_encoder_time:
            max_encoder_time = round(encoder_time, 3)
        if min_decoder_time is None or decoder_time < min_decoder_time:
            min_decoder_time = round(decoder_time, 3)
        if max_decoder_time is None or decoder_time > max_decoder_time:
            max_decoder_time = round(decoder_time, 3)

    avg_encoder_time = round(total_encoder_time / iterations, 3)
    avg_decoder_time = round(total_decoder_time / iterations, 3)

    uncompressed_bits = len(input_file)*8
    compressed_bits = encoded_file.length()
    compression_ratio = uncompressed_bits / compressed_bits
    print('Average encoder running time: ' + str(avg_encoder_time) + 'ms')
    print('Average decoder running time: ' + str(avg_decoder_time) + 'ms')
    print('Compression ratio: ' + str(compression_ratio))
    with open('output', 'a') as file:
        file.write(
            str(min_decoder_time) + '\n' + str(avg_decoder_time) + '\n' + str(max_decoder_time) + '\n' +
            str(min_encoder_time) + '\n' + str(avg_encoder_time) + '\n' + str(max_encoder_time) + '\n' +
            str(compression_ratio) + '\n')


def window_percentages(max__window_size, input_file):
    for percentage in range(10, 0, -2):
        percentage = percentage / 10
        print('---- Window Size: ' + str(int(percentage * 100)) + '% ----')
        window_size = int(max__window_size * percentage)
        # general_analysis(100, window_size, window_size, max__window_size)


with open('Input/Images/flower.bmp', 'rb') as file:
    myfile = file.read()
    print(myfile)
    window = len(myfile)
    print('input length '+str(window*8))
    # window_percentages(window, myfile)
    for percentage in range(10, 9, -1):
        percentage = percentage / 10
        encoded = encoder(2 ,int(percentage*window), int(percentage*window), myfile)
        print(len(encoded))
        print(str(window*8 / len(encoded)))

# with open('output', 'a') as file: 1903608, 2616699
#     file.write('------ new test ------\n')
#
# for length in range(1000, 52001, 1000):
#     print('------ '+str(length)+' ------')
#     window_percentages(length)


# with open('Input/Text/sentences.txt', 'rb') as file:
#     total_ratio = 0
#     count = 0
#     for line in file:
#         input = len(line)
#         input_size = input*8
#         encoded = encoder(input, input, line)
#         output = encoded.length()
#         total_ratio += input_size/output
#         count += 1
#     print(count)
#     average_compression_ratio = total_ratio / count
#     print('average compression ratio '+str(average_compression_ratio))


print(len(ascii_string(14).encode()))
print(len(ab_string(14).encode()))