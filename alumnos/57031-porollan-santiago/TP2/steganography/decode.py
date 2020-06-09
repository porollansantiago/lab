import multiprocessing as mp
import binascii


def create_processes(filename, offset, interleave, L):
    processes = []
    parent_conns = []
    for c in range(3):
        parent_conn, child_conn = mp.Pipe()
        p = mp.Process(target=get_msg, args=(child_conn, filename, c, offset, interleave, L))
        p.start()
        processes.append(p)
        parent_conns.append(parent_conn)
    return processes, parent_conns

def get_msg(conn, filename, c, offset, interleave, L):
    pixel_counter = 0
    if c != 2:
        L = (8 * L) // 3
    else:
        L = ((8 * L) // 3) + L % 8
    counter = 0
    msg = ""
    interleave_counter = interleave * 1
    while len(msg) < L:
        read = conn.recv()
        if read != 'stop':
            for byte in read:
                pixel_counter += 1
                if counter == c:
                    if pixel_counter > offset:
                        interleave_counter -= 1
                        if interleave_counter == 0:
                            interleave_counter = interleave * 1
                            if c == 0:
                                print(byte)
                            byte = list(format(byte, '08b'))
                            if c == 0:
                                print(byte)
                            msg += byte[7]
                            if len(msg) == L:
                                break
                counter += 1
                if counter == 3:
                    counter = 0
        else:
            break
    print(msg)


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))