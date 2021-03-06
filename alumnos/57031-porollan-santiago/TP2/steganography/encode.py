import os, threading, time
import multiprocessing as mp
from steganography.exceptions import InterleaveError


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


def create_file(filename, output_filename, sb, fd, offset, interleave, L):
    read = os.read(fd, sb)
    first_line = list(bytes('#UMCOMPU2 ' + str(offset) + " " + str(interleave) + " " + str(L) + "\n", encoding='utf=8'))
    read = list(read)
    for byte in first_line[::-1]:
        read.insert(3, byte)
    with open('output/'+output_filename, 'wb') as ni:
        ni.write(bytes(read))


def insert_into_file(filename, c, offset, interleave, conn, msg, sem, next_sem):
    counter = 0
    pixel_counter = 0
    msg_idx = 0
    L = len(msg)
    interleave_counter = 1
    if c != counter:
        sem.acquire()
        img = open('output/'+filename, 'ab')
    else:
        img = open('output/'+filename, 'ab')
    while True:
        read = conn.recv()
        if read != "stop":
            for byte in read:
                if counter == c:
                    pixel_counter += 1
                    if pixel_counter > offset and msg_idx < L:
                        interleave_counter -= 1
                        if interleave_counter == 0:
                            interleave_counter = interleave*1
                            byte = insert_into_byte(byte, msg, msg_idx)
                            msg_idx += 1
                    img.write(bytes([byte]))
                    img.flush()
                    release_sem(next_sem, c)
                    sem.acquire()
                counter += 1
                if counter == 3:
                    counter = 0
        else:
            next_sem.release()
            img.close()
            break


def insert_into_byte(byte, msg, msg_idx):
    byte = list(format(byte, "08b"))
    byte[7] = msg[msg_idx]
    return binaryToDecimal("".join(byte))


def release_sem(sem, c):
    while True:
        try:
            sem.release()
        except ValueError:
            pass
        else:
            break


def binaryToDecimal(binary): 
    binary = int(binary)
    decimal, i = 0, 0
    while(binary != 0): 
        dec = binary % 10
        decimal = decimal + dec * pow(2, i) 
        binary = binary//10
        i += 1
    return decimal


def validate_interleave(sb, width, height, offset, interleave, L):
    msg = sb + offset + interleave * L
    av = (width * height) * 3 - interleave - offset - sb
    print("espacio disponible:",av)
    print("espacio requerido:",msg)
    if msg <= av:
        return True
    raise(InterleaveError("Error. Revisar interleave"))
    
