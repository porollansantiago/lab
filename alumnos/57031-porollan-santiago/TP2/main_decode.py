import argparse, os, time, binascii
from steganography.prep import get_header_info
from steganography.decode import create_processes
from steganography.exceptions import HeaderKey, InterleaveError


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
    parser.add_argument('-o', '--offset', dest='offset', required=False, help='offset', default=-1)
    parser.add_argument('-i', '--interleave', dest='interleave', required=False, help='interleave', default=-1)
    parser.add_argument('-l', dest='L', required=False, help='msg size', default=-1)

    return parser.parse_args()


def send_r(fd, size, conns):
    stopped = [0, 0, 0]
    msg = ["", "", ""]
    while not (stopped[0] and stopped[1] and stopped[2]):
        read = os.read(fd, size)
        for i in range(3):
            if not stopped[i]:
                try:
                    conns[i].send(read)
                except:
                    if i == 2:
                        break
        for i in range(3):
            if not stopped[i]:
                if conns[i].poll():
                    byte = conns[i].recv()
                    if byte != 'stop':
                        msg[i] += byte
                    else:
                        stopped[i] = 1
    return msg


if __name__ == '__main__':
    start = time.time()
    args = get_args()
    try:
        fd = os.open(args.fn_img, os.O_RDONLY)
        header_info = get_header_info(args.fn_img, args.offset, args.interleave, args.L)
        
        processes, conns = create_processes(args.fn_img, header_info[2], header_info[3], header_info[4])
        header = os.read(fd, header_info[0])
        msg = send_r(fd, args.size, conns)
    except FileNotFoundError:
        print("Error. No se ha encontrado imagen:", args.fn_img)
    except MemoryError as exc:
        print("Error de memoria")
        for p in processes:
            p.terminate()
    except InterleaveError as exc:
        print(exc)
    except HeaderKey as exc:
        print(exc)
    else:
        print("Terminado con exito en: ", time.time()-start, "segundos")
        print('mensaje:')
        print('#######################################################')
        print(text_from_bits("".join(msg)))
        print('#######################################################')