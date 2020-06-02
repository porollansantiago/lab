

def histogram(number):
    return "#" * number

def histogram_from_file(filename="histogram"):
    l = [int(line.rstrip("\n")) for line in open(filename)]
    return list(map(histogram, l))

if __name__ == "__main__":

    l = []

    while True:
        n = input("Stop para terminar. Número: ")
        try:
            n = int(n)
        except:
            if n == "stop":
                break
            print("se deben ingresar números")
        else:
            l.append(n)

    for line in map(histogram, l):
        print(line)
