

def ej2_func(num, m, c=1, suma=0):
    if c-1 == m:
        return suma
    else:
        return ej2_func(num, m, c+1, suma + int(str(num) * c))
