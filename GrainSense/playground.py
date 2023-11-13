import sys

d = dict()
for i in range(50):
    d[i] = i
    print(sys.getsizeof(d))
