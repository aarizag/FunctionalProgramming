from pyrsistent import *

# Pvector
x = 1234124151125
vec = pvector(int(x) for x in str(x))
print(vec)

v1 = v(1, 2, 3,4,5,6,7,8)
v2 = v1.append(4)
v3 = v2.set(1, 5)

# print(v1, v2, v3, sep="\n")
# print(sum(v1[-2::-2]))

# PSet

