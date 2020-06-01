import argparse, os, time
import multiprocessing as mp


def get_color(color):
    if color == 0:
        return "red"
    if color == 1:
        return "green"
    if color == 2:
        return "blue"
    if color == 3:
        return "espejado"


def espejar(filename, conn, width=200):
    width *= 3
    # funcion target para el espejado
    newimage_arr = []
    lines=0
    while 1:
        data, remainder = conn.recv()
        if data == "stop":
            break
        data = list(data)
        while data:
            if remainder:
                newline += data[:remainder]
                L = len(data[:remainder])
            else:
                newline = data[remainder:width]
                L = len(newline)
            remainder = width - len(newline)
            for _ in range(L):
                data.pop(0)
            if len(newline) == width:
                linea_espejada = []
                for idx in range(0, len(newline),3):
                    linea_espejada.insert(0, newline[idx+2])
                    linea_espejada.insert(0, newline[idx+1])
                    linea_espejada.insert(0, newline[idx+0])

                escribir_archivo(filename, "espejado", linea_espejada)
                newimage_arr += newline
                lines+=1
                newline = []
        conn.send(remainder)
    print(lines)
    conn.send("finalizado espejado con exito")
        



def procesar_imagen(filename, color, added, conn):
    # funcion target
    # se determinan los valores a escribir en la nueva imagen
    # luego se escribe la imagen
    while 1:
        try:
            leido, count = conn.recv()
        except KeyboardInterrupt:
            print("\nProceso Hijo finalizado. Error con lectura de Pipe")
            exit(1)
        if leido == "stop":
            break
        newimage_arr = []
        for color_value in leido:
            # escribir bytes de la nueva imagen. dependiendo del color suma el valor
            if count == color:
                newl = int(color_value * added)
                newl = 255 if newl > 255 else newl
            else:
                newl = 0
            newimage_arr.append(newl)
            count += 1
            if count == 3:
                count = 0
        escribir_archivo(filename, get_color(color), newimage_arr)
        conn.send(count)
    conn.send("Filtro " + get_color(color) + " finalizado con exito")
    #if leido:
    #    try:
            # se vuelve a ejecutar la misma funcion para que el proceso quede esperando
    #        procesar_imagen(filename, color, added, conn)
    #    except RecursionError:
    #        print("Error. Buffer muy pequeño. Finalizar manualmente el programa")
    #        exit(1)

def escribir_archivo(filename, descr, newimage_arr):
    with open(filename[:-4] + "_" + descr + ".ppm", 'ab') as ni:
        ni.write(bytes(newimage_arr))

def escribir_headers(args, leido, espejado):
    # genera 3 procesos. se crean los archivos con sus headers para cada color
    processes = []
    exitcode = 0
    espejado = 1 if espejado else 0
    for color in range(3 + espejado):
        p = mp.Process(target=escribir_header, args=(args.archivo,
                                                     leido, color))
        p.start()
        processes.append(p)
    for process in processes:
        process.join()
        exitcode = exitcode or process.exitcode
    return exitcode


def escribir_header(filename, leido, color):
    # genera archivo segun el color con el header determinado
    with open(filename[:-4] + "_" + get_color(color) + ".ppm", 'wb') as ni:
        ni.write(bytes(list(leido)))


def get_arguments():
    parser = argparse.ArgumentParser(description="Procesar imagen. Generar 3 filtros de color")
    parser.add_argument("-f", dest="archivo", type=str,
                        help="Nombre de la imagen formato ppm", required=True)
    parser.add_argument("-n", dest="tam", type=int, metavar="SIZE",
                        required=True, help="Tamaño del bloque de bytes",
                        default=256)
    parser.add_argument("-r", dest="red", type=float, default=[1.1], metavar="RED",
                        nargs=1, help="Valor color rojo")
    parser.add_argument("-g", dest="green", type=float, default=[1.1], metavar="GREEN",
                        nargs=1, help="Valor color verde")
    parser.add_argument("-b", dest="blue", type=float, default=[1.1], metavar="BLUE",
                        nargs=1, help="Valor color azul")
    parser.add_argument("-e", "--espejar", dest="espejar", action='store_true', default=False,
                        help="Realizar espejado horizontal")
    return parser.parse_args()


def get_sb(filename):
    # cuenta las lineas validas. cuando obtiene 3 devuelve el indice del byte
    validlines = 0
    ignore_line = 0
    for idx, val in enumerate(open(filename, 'rb').read()):
        if validlines == 3:
            return idx
        if val == 35:
            ignore_line = 1
        elif ignore_line and val == 10:
            ignore_line = 0
        elif not ignore_line and val == 10:
            validlines += 1
    return 15


if __name__ == '__main__':
    args = get_arguments()
    try:
        fd = os.open(args.archivo, os.O_RDONLY)
    except FileNotFoundError:
        exitcode = 1
        print("No se ha encontrado el archivo. Finalizar manualmente el programa")
    else:
        exitcode = 0
    child_conns = [None, None, None, None]
    parent_conns = [None, None, None, None]
    parent_conns[0], child_conns[0] = mp.Pipe()
    parent_conns[1], child_conns[1] = mp.Pipe()
    parent_conns[2], child_conns[2] = mp.Pipe()
    parent_conns[3], child_conns[3] = mp.Pipe()

    # escribir header
    tiempo_inicial = time.time()
    if not exitcode:
        leido = os.read(fd, get_sb(args.archivo))
        exitcode = escribir_headers(args, leido, args.espejar)

    # escribir el resto
    colors = [args.red[0], args.green[0], args.blue[0]]
    espejado_int = 1 if args.espejar else 0
    counts = [0 for _ in range(3 + espejado_int)]
    processes = []

    for color in range(3):
        # se generan 3 procesos que quedan esperando recibir informacion
        p = mp.Process(target=procesar_imagen,
                       args=(args.archivo, color, colors[color],
                             child_conns[color]))
        p.start()
        processes.append(p)
    width=200
    # proceso que se dedica al espejado
    if args.espejar:
        p = mp.Process(target=espejar, args=(args.archivo, child_conns[3], width))
        p.start()
        processes.append(p)
    
    while not exitcode and leido:
        # se lee el archivo y se mandan los datos a los hijos
        try:
            leido = os.read(fd, args.tam)
        except MemoryError:
            exitcode = 1
            print("Error de memoria")
            continue
        for color in range(3):
            # se manda lo leido
            if leido:
                parent_conns[color].send((leido, counts[color]))
                if args.espejar and color == 0:
                    parent_conns[3].send((leido, counts[3]))
            else:
                parent_conns[color].send(("stop", counts[color]))
                if args.espejar and color == 0:
                    parent_conns[3].send(("stop", counts[3]))
                if color == 2:
                    break
        for color in range(3 + espejado_int):
            # se recibe la variable count
            # count puede tomar valores del 0 al 2 incluido
            # representa el ultimo color escrito por cada hijo
            try:
                counts[color] = parent_conns[color].recv()
                if type(counts[color]) is str:
                    print(counts[color])
            except KeyboardInterrupt:
                print("\nProceso Padre finalizado. Error con lectura de Pipe")
                exit(1)
    for process in processes:
        # se espera a que terminen los hijos
        try:
            process.join()
        except KeyboardInterrupt:
            print("\nContinuando proceso Padre")
            exitcode = 1
        exitcode = exitcode or process.exitcode

    # se muestra por pantalla informacion de la ejecucion
    tiempo_final = time.time()
    if not exitcode:
        print("Se generaron correctamente los 3 filtros")
    else:
        print("Ha ocurrido un error")
    print("Completado en", tiempo_final - tiempo_inicial, "segundos")
