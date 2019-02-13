open('format', 'w').close()
with open('format', 'a') as f:
    f.write('min decoder time \n')

with open('output') as fp:
    for index, line in enumerate(fp, 0):
        if index / 7 == int(index / 7):
            with open('format', 'a') as f:
                f.write(line)

with open('format', 'a') as f:
    f.write('\n')
    f.write('avg decoder time \n')

with open('output') as fp:
    for index, line in enumerate(fp, 6):
        if index / 7 == int(index / 7):
            with open('format', 'a') as f:
                f.write(line)

with open('format', 'a') as f:
    f.write('\n')
    f.write('max decoder time \n')

with open('output') as fp:
    for index, line in enumerate(fp, 5):
        if index / 7 == int(index / 7):
            with open('format', 'a') as f:
                f.write(line)

with open('format', 'a') as f:
    f.write('\n')
    f.write('min encoder time \n')

with open('output') as fp:
    for index, line in enumerate(fp, 4):
        if index / 7 == int(index / 7):
            with open('format', 'a') as f:
                f.write(line)

with open('format', 'a') as f:
    f.write('\n')
    f.write('avg encoder time \n')

with open('output') as fp:
    for index, line in enumerate(fp, 3):
        if index / 7 == int(index / 7):
            with open('format', 'a') as f:
                f.write(line)

with open('format', 'a') as f:
    f.write('\n')
    f.write('max encoder time \n')

with open('output') as fp:
    for index, line in enumerate(fp, 2):
        if index / 7 == int(index / 7):
            with open('format', 'a') as f:
                f.write(line)

with open('format', 'a') as f:
    f.write('\n')
    f.write('compression ratio \n')

with open('output') as fp:
    for index, line in enumerate(fp, 1):
        if index / 7 == int(index / 7):
            with open('format', 'a') as f:
                f.write(line)

with open('format', 'a') as f:
    f.write('\n')
