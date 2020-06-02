import argparse


def resta(a):
    return a[0] - a[1]


def mult(a):
    return a[0] * a[1]


def div(a):
    return a[0] / a[1]


# calculo s -t int 1 2
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='process some integers')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('nums', metavar='N', type=int, nargs=2, help='numeros para realizar un calculo')
    parser.add_argument('-t', '--tipo', dest="tipo", default="float", type=str, choices=['int', 'float', 'long'], help='tipo')
    group.add_argument('-s', '--suma', dest='operator_s', action='store_const', const=sum, default=0, help='suma')
    group.add_argument('-r', '--resta', dest='operator_r', action='store_const', const=resta, default=0, help='resta')
    group.add_argument('-m', '--mult', dest='operator_m', action='store_const', const=mult, default=0, help='multiplicacion')
    group.add_argument('-d', '--div', dest='operator_d', action='store_const', const=div, default=0, help='division')
    args = parser.parse_args()
    print(eval(args.tipo)((args.operator_s or args.operator_r or args.operator_m or args.operator_d)(args.nums)))
