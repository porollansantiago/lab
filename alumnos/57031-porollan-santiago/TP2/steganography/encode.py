import os
import multiprocessing as mp


def create_file(filename, output_filename, sb, fd):
    read = os.read(fd, sb)
    with open('output/'+output_filename, 'wb') as ni:
        ni.write(bytes(list(read)))


def create_processes(filename, header_info):
    offset, interleave = header_info[2], header_info[3]
    processes = []
    parent_conns = []
    for c in range(3):
        parent_conn, child_conn = mp.Pipe()
        p = mp.Process(target=insert_into_file, args=(filename, c, offset, interleave, child_conn))
        p.start()
        parent_conns.append(parent_conn)
        processes.append(p)
    return processes, parent_conns


def insert_into_file(filename, c, offset, interleave, conn):
    while True:
        read = conn.recv()
        # print(os.getpid(), read)
