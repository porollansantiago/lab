import signal
import time
import os


def handler(nro, frame):
    global sleep_time
    sleep_time *= 2


def alarm_handler(nro, frame):
    global sleep_time
    global real
    real += 1
    signal.alarm(sleep_time)
    print(real)


print(os.getpid())
sleep_time = 1
real = 1
signal.alarm(sleep_time)
signal.signal(signal.SIGALRM, alarm_handler)
signal.signal(signal.SIGUSR1, handler)
time.sleep(200)
