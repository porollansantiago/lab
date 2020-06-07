

def get_msg(filename):
    with open(filename, 'r') as fle:
        read = fle.read()
    L = len(read)
    size = L // 3
    return ["".join([format(ord(c), "08b") for c in read[: size]]),
            "".join([format(ord(c), "08b") for c in read[size: 2*size]]),
            "".join([format(ord(c), "08b") for c in read[2*size:]])], L


def convert_to_binary(s):
    return "".join([format(ord(c), "08b") for c in s])


def get_header_info(filename, offset=0, interleave=0):
    validlines = 0
    ignore_line = 0
    width = ""
    fl = open(filename, 'rb')
    for idx, val in enumerate(fl.read()):
        if validlines == 1 and not ignore_line:
            if val in range(48, 58) and len(width) != 3:
                width += str(val-48)
        if validlines == 3:
            fl.close()
            return (idx, int(width), offset, interleave)
        if val == 35:
            ignore_line = 1
        elif ignore_line and val == 10:
            ignore_line = 0
        elif not ignore_line and val == 10:
            validlines += 1