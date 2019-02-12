from LZ77 import encoder, decoder
import time
from random import randint


def generate_bitstring(length):
    bitstring = ''
    for bit in range(length):
        bitstring += str(randint(0, 1))
    return bitstring.encode()


# Analyses performance in all areas on a single input and takes average of 3 attempts for running times
def general_analysis(window_size, buffer_size, input_file):
    encoded_file = None
    total_encoder_time = 0
    total_decoder_time = 0
    iterations = 1

    for iteration in range(iterations):
        time_stamp1 = time.time() * 1000
        encoded_file = encoder(window_size, buffer_size, input_file)
        time_stamp2 = time.time() * 1000
        decoder(window_size, buffer_size, encoded_file)
        time_stamp3 = time.time() * 1000
        encoder_time = time_stamp2 - time_stamp1
        decoder_time = time_stamp3 - time_stamp2
        total_encoder_time += encoder_time
        total_decoder_time += decoder_time
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
            str(avg_encoder_time) + '\n' + str(avg_decoder_time) + '\n'
            + str(compression_ratio) + '\n')


def encoder_analysis(iterations, window_size, buffer_size, input_data):
    print('------ Conducting Encoder Analysis -----' + '\n' + 'Window size, W: ' + str(window_size) + '\n' +
          'Lookahead Buffer size, L: ' + str(buffer_size) + '\n' + 'Number of iterations: ' + str(iterations) + '\n')

    min_run_time = None
    max_run_time = None
    total_run_time = 0
    for iteration in range(iterations):
        start_time = time.time() * 1000  # time in milli seconds
        encoder(window_size, buffer_size, input_data)
        stop_time = time.time() * 1000  # time in milli seconds
        run_time = stop_time - start_time
        total_run_time += run_time
        if min_run_time is None or run_time < min_run_time:
            min_run_time = round(run_time, 3)
        if max_run_time is None or run_time > max_run_time:
            max_run_time = round(run_time, 3)

    avg_run_time = round(total_run_time / iterations, 3)

    print('Minimum running time: ' + str(min_run_time) + '\n' + 'Average running time: ' + str(avg_run_time) + '\n'
          + 'Maximum running time: ' + str(max_run_time) + '\n')

    with open('output', 'a') as file:
        file.write(
            str(min_run_time) + '\n' + str(avg_run_time) + '\n'
            + str(max_run_time) + '\n')


def window_percentages(max__window_size, input_file):
    for percentage in range(1, 21):
        percentage = percentage / 20
        print('---- Window Size: ' + str(int(percentage * 100)) + '% ----')
        window_size = int(max__window_size * percentage)
        general_analysis(window_size, window_size, input_file)


with open('Input/short_example', 'rb') as file:
    myfile = file.read()
    window = len(myfile)
    # window_percentages(window, myfile)
    # general_analysis(500, 500, myfile)
    encoded = encoder(window, window, myfile)
    print(decoder(window, window, encoded))

