

def histogram(number):
    return "#" * number

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
