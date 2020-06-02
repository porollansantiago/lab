import signal
import os
import sys
import argparse
import time

global filename
global s


def pasar_mayusc(nro, fram):
    print("pasando a mayus")
    fil = [line.upper() for line in open(filename, 'r')]
    with open(filename, 'w') as f:
        f.write("".join(fil))


if __name__ == '__main__':
    print("padre", os.getpid())
    r, w = os.pipe()
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='filename', type=str, help='nombre del archivo')
    args = parser.parse_args()
    filename = args.filename
    s = "".join(sys.stdin)
    signal.signal(signal.SIGUSR1, pasar_mayusc)
    pid1 = os.fork()
    if pid1 == 0:
        print("hijo lector", os.getpid())
        time.sleep(4)
        exit()
    pid2 = os.fork()
    if pid2 == 0:
        print("hijo escritor", os.getpid())
        with open(filename, 'w') as f:
            print("escribiendo")
            f.write(s)
        os.kill(pid1, signal.SIGUSR1)
        exit()
