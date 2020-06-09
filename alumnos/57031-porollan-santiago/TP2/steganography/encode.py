import os, threading, time
import multiprocessing as mp


def create_file(filename, output_filename, sb, fd):
    read = os.read(fd, sb)
    with open('output/'+output_filename, 'wb') as ni:
        ni.write(bytes(list(read)))


def create_processes(filename, header_info, msg, L):
    offset, interleave = header_info[2], header_info[3]
    processes = []
    parent_conns = []
    sems = []
    for _ in range(3):
        new_sem = mp.BoundedSemaphore()
        new_sem.acquire()
        sems.append(new_sem)
    for c in range(3):
        parent_conn, child_conn = mp.Pipe()
        i = c+1 if c+1 != 3 else 0
        p = mp.Process(target=insert_into_file,
                       args=(filename, c, offset,
                             interleave, child_conn,
                             msg[c], sems[c], sems[i]))
        p.start()
        parent_conns.append(parent_conn)
        processes.append(p)
    return processes, parent_conns


def insert_into_file(filename, c, offset, interleave, conn, msg, sem, next_sem):
    counter = 0
    if c != counter:
        print(c, "bloqueado")
        sem.acquire()
        print(c, "continua")
        img = open('output/'+filename, 'ab')
    else:
        img = open('output/'+filename, 'ab')
    while True:
        read = conn.recv()
        if read != "stop":
            print("holaaa", c)
            color_values = []
            for byte in read:
                if counter == c:
                    color_values.append(byte)
                counter += 1
                if counter == 3:
                    counter = 0
            for color_value in color_values:
                print(c, "escribe")
                img.write(bytes([color_value]))
                img.flush()
                # write(filename, [color_value])
                while True:
                    try:
                        next_sem.release()
                    except ValueError:
                        pass
                    else:
                        print("process",c,"libera",c+1)
                        break
                print(c,"bloqueado")
                sem.acquire()
                print(c,"continua")
        else:
            next_sem.release()
            img.close()
            break

        

def write(filename, newimage_arr):
    with open('output/'+filename, 'ab') as ni:
        ni.write(bytes(newimage_arr))
