import argparse
import os
import signal
global archivo


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, nargs=1, help='nombre del archivo')
    parser.add_argument('time', type=int, nargs=1, help='tiempo de espera')
    return parser.parse_args()


def write(fname):
    print("Guardando en archivo...")
    with open(fname, 'w') as fn:
        for filename in os.listdir():
            fn.write(filename+"\n")


def readfile(nro, frame):
    print("Leyendo archivo: ")
    pid = os.fork()
    if pid == 0:
        print(open(archivo, 'r').read())
        exit()
    os.wait()


if __name__ == '__main__':
    args = get_arguments()
    archivo = args.filename[0]
    write(args.filename[0])
    print("Esperando ", args.time[0], " segundos")
    signal.alarm(args.time[0])
    signal.signal(signal.SIGALRM, readfile)

    input()
