import cmath
from math import sqrt, log2
from functools import reduce

from numpy import zeros, nan
from matplotlib import cm
from matplotlib.colors import Normalize

from cv2 import imwrite


# evaluates the polynomial p at point z
def horner(p, z):
    return reduce(lambda x, y: x * z + y, p)

def escapetime(p, z, R, K):
    k, zk = 1, z
    while k < K and abs(zk) <= R:
        zk = horner(p, zk)
        k += 1
    return k

def drawImage(filename, rgbfun, n):
    colormat = zeros((n, n, 3), dtype=float)
    for i in range(n):
        for j in range(n):
            rgb01 = rgbfun(i, j) # rgb(a) values in [0,1]
            for k in range(3): 
                colormat[i,j,k] = int(255 * rgb01[2-k])
    imwrite(filename, colormat)

def mapToComplexPlaneCenter(n, c, r, i, j):
    return c + r * complex(2 * j / n - 1, 2 * i / n - 1)

def drawEscapetimeMandelbrot(n, ctr, r, colormap, K):
    q = lambda c: [1, 0, c]
    
    def rgbfun(i, j):
        c = mapToComplexPlaneCenter(n, ctr, r, i, j)
        k = escapetime(q(c), 0, 2, K)
        return colormap(k/K) if k < K else (0,0,0)

    drawImage('escapetime_mandelbrot.png', rgbfun, n)

def radiusJulia(poly, L=1.0000001):
    n = len(poly) - 1
    an = abs(poly[0])
    C = sum(map(abs, poly)) - an
    return max(1, 2 * C / 2, pow(2 * L / an, 1 / (n-1)))

# L > 1 should be as close to 1 as possible
def radiusJulia(poly, L=1.0000001):
    n = len(poly) - 1
    an = abs(poly[0])
    C = sum(map(abs, poly)) - an
    return max(1, 2 * C / 2, pow(2 * L / an, 1 / (n-1)))

def drawEscapetimeJulia(n, p, colormap, K):
    rp = radiusJulia(p)
    
    def rgbfun(i, j):
        z = mapToComplexPlaneCenter(n, 0, rp, i, j)
        k = escapetime(p, z, rp, K)
        return colormap(k/K) if k < K else (0,0,0)
    
    drawImage('escapetime_julia.png', rgbfun, n)

def demMandelbrot(c, K, overflow):
    ck, dk = c, 1
    for _ in range(K):
        if max(
            abs(ck.real), abs(ck.imag),
            abs(dk.real), abs(dk.imag)
        ) > overflow: break
        dk = 2 * ck * dk + 1
        ck *= ck
        ck += c
    absck = abs(ck)
    if absck <= 2: return 0
    else:
        absdk = abs(dk)
        if absdk == 0: return nan # this will probably never happen
        estimate = log2(absck) * absck / absdk
        return -log2(estimate)


def demMandelbrot(c, K, overflow):
    ck, dk = c, 1
    for _ in range(K):
        if max(
            abs(ck.real), abs(ck.imag),
            abs(dk.real), abs(dk.imag)
        ) > overflow: break # so computer doesn't crash
        dk *= 2 * ck
        dk += 1
        ck *= ck
        ck += c
    absck = abs(ck)
    if absck <= 2: return 0
    else:
        absdk = abs(dk)
        if absdk == 0: return nan # this will probably never happen
        estimate = log2(absck) * absck / absdk
        return -log2(estimate)

def drawDemMandelbrot(n, ctr, r, colormap, K, overflow):
    arr = zeros((n, n), dtype=float)
    
    for i in range(n):
        for j in range(n):
            c = mapToComplexPlaneCenter(n, ctr, r, i, j)
            arr[i,j] = demMandelbrot(c, K, overflow)

    m, M = arr.min(), arr.max()
    arr[arr == 0] = M # 0 only denotes the inner set and it could spoil our normalization
    arr[arr == nan] = m # we don't care, this happens too rarely, if at all
    colortable = colormap(Normalize(m, M)(arr))
    
    def rgbfun(i, j):
        if arr[i,j] == M: return (0,0,0)
        else: return colortable[i,j]

    drawImage('demMandelbrot.png', rgbfun, n)

# derivative of the given polynomial
def differentiate(poly):
    n, an = len(poly) - 1, poly[0]
    return [(n - i) * an for (i, an) in enumerate(poly[:-1])]

def demJulia(p, dp, z, K, R, overflow):
    zk, dk = z, 1
    for _ in range(K):
        if max(
            abs(zk.real), abs(zk.imag),
            abs(dk.real), abs(dk.imag)
        ) > overflow: break
        dk = horner(dp, zk) * dk
        zk = horner(p, zk)
    abszk = abs(zk)
    if abszk < R: return 0
    else:
        absdk = abs(dk)
        if absdk == 0: return nan
        estimate = log2(abszk) * abszk / absdk
        return -log2(estimate)

def drawDemJulia(n, p, colormap, K, pow_, overflow):
    arr = zeros((n, n), dtype=float)
    dp = differentiate(p)
    r = radiusJulia(p, 1.000001)

    for i in range(n):
        for j in range(n):
            z = mapToComplexPlaneCenter(n, 0, r, i, j)
            arr[i,j] = demJulia(p, dp, z, K, r, overflow)

    m, M = arr.min(), arr.max()
    arr[arr == 0] = M
    arr[arr == nan] = M
    normalized = Normalize(m, M)(arr)
    adjusted = pow(normalized, pow_)
    colortable = colormap(adjusted)
            
    def rgbfun(i, j):
        if arr[i,j] == M: return (0,0,0)
        else: return colortable[i,j]

    drawImage('demJulia.png', rgbfun, n)
    

def inCardioidOrCircle(c):
    s = cmath.sqrt(1 - 4 * c)
    return abs(1 + s) <= 1 or abs(1 - s) <= 1 or abs(1 + c) <= 1/4


if __name__ == '__main__':
    
    drawEscapetimeJulia(
      500, [1, 0, -0.7508387093588403-0.046j],
      cm.inferno.reversed(), 250
    )
