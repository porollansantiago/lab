import argparse
import os
import signal
import time
from random import randint
global sleep_time
r, w = os.pipe()
global pid2


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('sleep_time', metavar="T", nargs=1, type=int, help='Tiempo de espera')
    return parser.parse_args().sleep_time[0]


def get_number(nro, frame):
    global w
    global r
    signal.alarm(sleep_time)
    num = randint(-1000, 1000)
    print("PID: ", os.getpid(), " PPID: ", os.getppid(), " Enviando ", num)
    os.write(w, str(num).encode())
    os.kill(pid2, signal.SIGUSR1)


def show_num(nro, frame):
    global w
    global r
    # w.close()
    num = os.read(r, 100)
    print("PID: ", os.getpid(), " PPID: ", os.getppid(), " Recibido: ", int(num))
    print("Esperando ", sleep_time, " segundos")


if __name__ == '__main__':
    sleep_time = get_arguments()
    print("Parent PID: ", os.getpid())
    signal.signal(signal.SIGALRM, get_number)
    signal.signal(signal.SIGUSR1, show_num)
    pid2 = os.fork()
    if pid2 == 0:
        time.sleep(200)
        exit()
    pid1 = os.fork()
    if pid1 == 0:
        print("Esperando ", sleep_time, " segundos")
        signal.alarm(sleep_time)
        time.sleep(200)
        exit()
    os.wait()
