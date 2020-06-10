import argparse, os, time, binascii
from steganography.prep import get_header_info
from steganography.decode import create_processes


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)


def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def get_args():
    parser = argparse.ArgumentParser(description='image steganography decoder')
    parser.add_argument('-f', '--file', dest='fn_img', required=True, help='input img')
    parser.add_argument("-n", dest="size", type=int, metavar="SIZE",
                        required=True, help="Tamaño del bloque de bytes")
    parser.add_argument('-o', '--offset', dest='offset', required=False, help='offset', default=0)
    parser.add_argument('-i', '--interleave', dest='interleave', required=False, help='interleave', default=0)
    return parser.parse_args()


if __name__ == '__main__':
    start = time.time()
    args = get_args()
    fd = os.open(args.fn_img, os.O_RDONLY)
    header_info = get_header_info(args.fn_img, args.offset, args.interleave)
    processes, conns = create_processes(args.fn_img, header_info[2], header_info[3], header_info[4])
    header = os.read(fd, header_info[0])
    flag = 1
    while flag:
        read = os.read(fd, args.size)
        for i in range(3):
            try:
                conns[i].send(read)
            except BrokenPipeError:
                flag = 0
    msg = ''
    for i in range(3):
        msg += conns[i].recv()
    print("benchmark: ", time.time() - start)
    print('mensaje:')
    print('#######################################################')
    print(text_from_bits(msg))
    print('#######################################################')