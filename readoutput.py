open('format', 'w').close()
with open('output') as fp:
    for index, line in enumerate(fp, 0):
        if index / 3 == int(index / 3):
            with open('format', 'a') as f:
                f.write(line)

with open('format', 'a') as f:
    f.write('\n')

with open('output') as fp:
    for index, line in enumerate(fp, 2):
        if index / 3 == int(index / 3):
            with open('format', 'a') as f:
                f.write(line)

with open('format', 'a') as f:
    f.write('\n')

with open('output') as fp:
    for index, line in enumerate(fp, 1):
        if index / 3 == int(index / 3):
            with open('format', 'a') as f:
                f.write(line)

with open('format', 'a') as f:
    f.write('\n')
