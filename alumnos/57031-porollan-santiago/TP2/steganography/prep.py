from steganography.exceptions import EmptyMsg, HeaderKey, InterleaveError


def get_msg(filename):
    with open(filename, 'r') as fle:
        read = fle.read()
    if not read:
        raise EmptyMsg("Error. Mensaje vacío")
    print("guardando mensaje:")
    print('#######################################################')
    print(read)
    print('#######################################################')
    read = "".join([format(ord(c), "08b") for c in read])
    L = len(read)
    size = L // 3
    return [read[: size], read[size: 2*size], read[2*size:]], L


def convert_to_binary(s):
    return "".join([format(ord(c), "08b") for c in s])


def get_header_info(filename, offset=0, interleave=0, L=0):
    validlines = 0
    ignore_line = 0
    width = ""
    width_flag = 1
    height_flag = 1
    height = ""
    possible_msg = 1
    key = []
    msg_flag = 0
    umcompu2 = [35, 85, 77, 67, 79, 77, 80, 85, 50]
    offset_interleave = ["", "", ""]
    oi_idx = -1
    fl = open(filename, 'rb')
    for idx, val in enumerate(fl.read()):
        if validlines == 1:
            if msg_flag:
                msg_flag, oi_idx= get_offset_interleave(val, msg_flag, oi_idx, offset_interleave)
            elif possible_msg:
                possible_msg, msg_flag = check_if_msg(val, key, possible_msg, umcompu2, msg_flag)
            if not ignore_line:
                if val in range(48, 58):
                    if width_flag:
                        width += str(val-48)
                    elif height_flag:
                        height += str(val-48)
                elif val == 32:
                    width_flag = 0
        if validlines == 3:
            fl.close()
            offset = int(offset_interleave[0]) if offset_interleave[0] else offset
            interleave = int(offset_interleave[1]) if offset_interleave[1] else interleave
            if interleave <= 0:
                if interleave == -1:
                    raise InterleaveError("Error. El archivo no contiene mensaje")
                else:
                    raise InterleaveError("Error. Revisar interleave")
            if offset <= 0:
                raise InterleaveError("Error. Revisar offset")
            L = offset_interleave[2] if offset_interleave[2] else L
            return (idx, int(width), offset, interleave, int(L), int(height))
        if val == 35:
            ignore_line = 1
        elif ignore_line and val == 10:
            ignore_line = 0
        elif not ignore_line and val == 10:
            validlines += 1


def get_offset_interleave(val, msg_flag, oi_idx, offset_interleave):
        if val == 10:
            msg_flag = 0
        elif val == 32:
            oi_idx += 1
        else:
            try:
                offset_interleave[oi_idx] += str(val-48)
            except IndexError:
                msg_flag = 0
        return msg_flag, oi_idx


def check_if_msg(val, key, possible_msg, umcompu2, msg_flag):
    key.append(val)
    if key != umcompu2[:len(key)]:
        possible_msg = 0
    elif len(umcompu2) == len(key):
        msg_flag = 1
    return possible_msg, msg_flag