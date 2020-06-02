import multiprocessing
import argparse
import os


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', choices=os.listdir(), nargs=1, type=str, help='Nombre de archivo')
    return parser.parse_args().filename[0]


def readline(line, conn):
    new_line = []
    line = line.replace("\n", "")
    print(os.getpid(), " leyendo: ", line)
    for word in line.split():
        new_line.append(word.upper()[::-1])
    conn.send(" ".join(new_line))


if __name__ == '__main__':
    print("Parent: ", os.getpid())
    archivo = get_arguments()
    parent_conn, child_conn = multiprocessing.Pipe()
    with open(archivo, 'r') as ar:
        for line in ar.readlines():
            p = multiprocessing.Process(target=readline, args=(line, child_conn))
            p.start()
            print(os.getpid(), "recibiendo: ", parent_conn.recv())
