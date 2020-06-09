import argparse, os, time
from steganography.prep import get_header_info
from steganography.decode import create_processes


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
    with open('dummy.ppm', 'wb') as f:
        f.write(header)
    while True:
        read = os.read(fd, args.size)
        if not read:
            read = 'stop'
        for i in range(3):
            conns[i].send(read)
        if read == 'stop':
            break
    print("benchmark: ", time.time() - start)
