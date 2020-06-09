import multiprocessing as mp


def create_processes(filename):
    processes = []
    parent_conns = []
    for c in range(3):
        parent_conn, child_conn = mp.Pipe()
        p = mp.Process(target=get_msg, args=(child_conn, filename, c))
        p.start()
        processes.append(p)
        parent_conns.append(parent_conn)
    return processes, parent_conns

def get_msg(conn, filename, c):
    while True:
        read = conn.recv()
        if read == 'stop':
            break
        print(c)