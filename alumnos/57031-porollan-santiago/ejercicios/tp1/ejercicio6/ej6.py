

def sort(ar):
    L = len(ar)
    n = 1
    while n != L:
        for idx in range(L-n):
            if ar[idx] < ar[idx + 1]:
                ar[idx] = ar[idx] ^ ar[idx + 1]
                ar[idx + 1] = ar[idx] ^ ar[idx + 1]
                ar[idx] = ar[idx] ^ ar[idx + 1]
        n += 1
    return ar
        