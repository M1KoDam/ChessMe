from math import gcd


def sgn(num):
    if num > 0:
        return 1
    if num < 0:
        return -1
    return 0


def sgn_vector(v):
    vector_gcd = gcd(v[0], v[1])
    return v[0] // vector_gcd, v[1] // vector_gcd
