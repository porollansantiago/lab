import argparse
import os
import math


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calcular potencia')
    parser.add_argument('-n', dest='base', type=int, help='base', required=True)
    parser.add_argument('-c', dest='cant', type=int, help='cantidad de hijos', default=1)
    parser.add_argument('-v', '--verbose', dest='verb', action='store_const', const=True, default=False, help='modo verboso')
    args = parser.parse_args()
    if args.verb:
        print('argumentos ingresados: (\'-v\', \'\'), (\'-n\', \'',args.base,'\')')
        print('PID padre: ', os.getpid())
        print('Creando hijos')
    for _ in range(args.cant):
        pid = os.fork()
        if pid == 0:
            expon = int(input('\nexponente: '))
            #expon = 2
            if args.verb:
                print('PID hijo: ', os.getpid())
            print('potencia: ', args.base ** expon)
            if args.verb:
                print('Creado por: ', os.getppid())
            exit()
        os.wait()

