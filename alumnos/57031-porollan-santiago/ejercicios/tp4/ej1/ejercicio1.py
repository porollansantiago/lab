import argparse
import os


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', choices=os.listdir(), nargs=1, type=str, help='Nombre de archivo')
    return parser.parse_args().filename[0]


if __name__ == '__main__':
    archivo = get_arguments()
    r, w = os.pipe()
    with open(archivo, 'r') as ar:
        for line in ar.readlines():
            pid = os.fork()
            if pid == 0:
                line = line[:-1]
                print(os.getpid(), " leyendo: ", line)
                new_line = []
                if not line:
                    os.write(w, "Error".encode())
                    exit()
                for word in line.split():
                    new_line.append(word[::-1].upper())
                os.write(w, " ".join(new_line).encode())
                exit()
            os.wait()
            line = os.read(r, 100).decode()
            if line != "Error":
                print(os.getpid(), "recibiendo: ", line)
