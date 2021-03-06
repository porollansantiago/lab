import argparse, os, concurrent.futures, threading, time, random
from steganography.prep import get_msg, get_header_info
from steganography.encode import *
from steganography.exceptions import *

read = 1

def get_args():
    parser = argparse.ArgumentParser(description="message-image encoding")
    parser.add_argument("-m", dest="fn_msg", type=str,
                        help="Nombre del archivo mensaje", required=True)
    parser.add_argument("-f", dest="fn_img", type=str,
                        help="Nombre de la imagen formato ppm", required=True)
    parser.add_argument("-o", dest="fn_out", type=str,
                        help="Nombre de la imagen formato ppm", required=True)
    parser.add_argument("-n", dest="size", type=int, metavar="SIZE",
                        required=True, help="Tamaño del bloque de bytes")
    parser.add_argument("-e","--offset", dest="offset", type=int, metavar="pixels",
                        required=True, help="Valor del Offset")
    parser.add_argument("-i","--interleave", dest="interleave", type=int, metavar="pixels",
                        required=True, help="Valor del Interleave")
    return parser.parse_args()

def send_data1(x, conn, read):
    conn.send(read)
    print("thread: ", x, "read: ", read)


def concurret_futures():
    global read
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    data = [x for x in range(1, 16000)]
    ind = 0
    while read:
        try:
            read = data[ind]
        except:
            break
        ind += 1
        concurrent.futures.wait([executor.submit(send_data1, x, parent_conns[x], read) for x in range(3)])
        print("all done")


def threading_and_sem():
    global read
    sems = []
    sems_p = []
    # sem_p = threading.Semaphore()
    for i in range(3):
        nsem = threading.BoundedSemaphore()
        nsem.acquire()
        semp = threading.BoundedSemaphore()
        semp.acquire()
        t = threading.Thread(target=send_data, args=(i, parent_conns[i], nsem, semp))
        t.start()
        sems.append(nsem)
        sems_p.append(semp)
    while read:
        read = os.read(fd, args.size)
        if not read:
            read = 'stop'
        for sem11 in sems:
            while 1:
                try:
                    sem11.release()
                except:
                    pass
                else:
                    break
        if read == 'stop':
            break
        for sempp in sems_p:
            sempp.acquire()

def send_data(x, conn, sem, semp):
    # threading and sem
    while True:
        sem.acquire(1)
        conn.send(read)
        if read == 'stop':
            break
        while 1:
            try:
                semp.release()
            except ValueError:
                pass
            else:
                break

def serie(fd, size):
    read = 1
    while read:
        read = os.read(fd, size)
        for x in range(3):
            if read:
                parent_conns[x].send(read)
            else:
                parent_conns[x].send("stop")


if __name__ == '__main__':
    start = time.time()
    args = get_args()
    try:
        fd = os.open(args.fn_img, os.O_RDONLY)
        msg, L = get_msg(args.fn_msg)
        header_info = get_header_info(args.fn_img, args.offset, args.interleave, L)
        validate_interleave(header_info[0], header_info[1], header_info[5], header_info[2], header_info[3], header_info[4])
        create_file(args.fn_img, args.fn_out, header_info[0], fd, header_info[2], header_info[3], header_info[4])
        processes, parent_conns = create_processes(args.fn_out, header_info, msg, L)
        serie(fd, args.size)
        # threading_and_sem()
        for p in processes:
            p.join()
    except FileNotFoundError:
        print("Error. No se ha encontrado imagen:", args.fn_img)
    except InterleaveError as exc:
        print(exc)
    except EmptyMsg as exc:
        print(exc)
    except MemoryError as exc:
        print("Error de memoria")
        for p in processes:
            p.terminate()
    else:
        print("Terminado con exito en: ", time.time()-start, "segundos")
