import argparse
import multiprocessing as mp
import time
import os


def mult(line, escalar):
    num = ""
    new_line = []
    for x in line:
        if x.isnumeric():
            num += x
        else:
            if num:
                new_line.append(int(num)*escalar)
            num = ""
    return new_line
    # return [int(x)*escalar for x in line if x.isnumeric()]


def div(line, escalar):
    num = ""
    new_line = []
    for x in line:
        if x.isnumeric():
            num += x
        else:
            if num:
                new_line.append(int(num)/escalar)
            num = ""
    return new_line
    # return [int(x)/escalar for x in line if x.isnumeric()]


def processline(line, operacion, escalar, output, output_filename="matrix_output"):
    line = operacion(line, escalar)
    if output:
        with open(output_filename, 'a') as m:
            m.write(str(line)+'\n')
    else:
        print(line)


def processlines(lines, operacion, escalar, output):
    for lines1 in lines:
        for line in [x for x in lines1.split("\n") if x]:
            processline(line, operacion, escalar, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Procesar matriz")
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-i', '--input', dest='archivo', type=str, nargs=1, help='Nombre del archivo', required=True)
    group.add_argument('-m', dest='operacion', action='store_const', const=mult, help='Multiplicar por un escalar')
    group.add_argument('-d', dest='operacion', action='store_const', const=div, help='Dividir por un escalar')
    parser.add_argument('escalar', type=int, metavar='N', nargs=1, help="Escalar")
    parser.add_argument('-o', '--output', dest='output', action='store_true', help="File output")
    args = parser.parse_args()
    if args.output:
        f = open('matrix_output', 'w')
        f.close()

    start_time1 = time.time()

    # ultimo multiprocessing
    processes = []
    with open(args.archivo[0], 'r') as ar:
        lines = ar.readlines()
    linecount = len(lines)
    lines_per_process = linecount // mp.cpu_count()
    start = 0
    end = lines_per_process
    for _ in range(mp.cpu_count()):
        lines_to_process = lines[start:end]
        start += lines_per_process
        end += lines_per_process
        p = mp.Process(target=processlines, args=(lines_to_process, args.operacion, args.escalar[0], args.output))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
    remaining_lines_count = linecount % mp.cpu_count()
    remaining_lines = lines[-remaining_lines_count:]
    for line in remaining_lines:
        p = mp.Process(target=processline, args=(line, args.operacion, args.escalar[0], args.output))
        p.start()
        processes.append(p)
    for process in processes:
        process.join()
    end_time1 = time.time()

    # primer multiprocessing
    # with open(args.archivo[0], 'r') as ar:
    #     processes = []
    #    for line in ar.readlines():
    #        p = mp.Process(target=processline, args=(line, args.operacion, args.escalar[0], args.output))
    #        processes.append(p)
    #        p.start()
    # for process in processes:
    #     process.join()

    # sin multiprocessing
    
    with open(args.archivo[0], 'r') as ar:
        for line in ar.readlines():
            processline(line, args.operacion, args.escalar[0], args.output, "no_multiproc")
    end_time2 = time.time()

    print("multiprocessing: ", end_time1 - start_time1)
    print("normal: ", end_time2 - end_time1)
