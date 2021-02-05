import cython
cimport cython
import numpy as np
cimport numpy as np
from numpy cimport ndarray
from Vector4 import Vector4
from cython.parallel import prange, parallel
from cython cimport floating
from libc.math cimport sqrt
from cpython cimport array
import array
from threading import Thread

ctypedef unsigned char[:, :] surface_type


cpdef list InverseMatrix(
        float A00, float A01, float A02, float A03,
        float A10, float A11, float A12, float A13,
        float A20, float A21, float A22, float A23,
        float A30, float A31, float A32, float A33,):
    cdef float A2323 = A22 * A33 - A23 * A32
    cdef float A1323 = A21 * A33 - A23 * A31
    cdef float A1223 = A21 * A32 - A22 * A31
    cdef float A0323 = A20 * A33 - A23 * A30
    cdef float A0223 = A20 * A32 - A22 * A30
    cdef float A0123 = A20 * A31 - A21 * A30
    cdef float A2313 = A12 * A33 - A13 * A32
    cdef float A1313 = A11 * A33 - A13 * A31
    cdef float A1213 = A11 * A32 - A12 * A31
    cdef float A2312 = A12 * A23 - A13 * A22
    cdef float A1312 = A11 * A23 - A13 * A21
    cdef float A1212 = A11 * A22 - A12 * A21
    cdef float A0313 = A10 * A33 - A13 * A30
    cdef float A0213 = A10 * A32 - A12 * A30
    cdef float A0312 = A10 * A23 - A13 * A20
    cdef float A0212 = A10 * A22 - A12 * A20
    cdef float A0113 = A10 * A31 - A11 * A30
    cdef float A0112 = A10 * A21 - A11 * A20

    cdef float determinant = (A00 * (A11 * A2323 - A12 * A1323 + A13 * A1223) -
                              A01 * (A10 * A2323 - A12 * A0323 + A13 * A0223) +
                              A02 * (A10 * A1323 - A11 * A0323 + A13 * A0123) -
                              A03 * (A10 * A1223 - A11 * A0223 + A12 * A0123))

    determinant = 1 / determinant
    return [determinant * (A11 * A2323 - A12 * A1323 + A13 * A1223),
            determinant * - (A01 * A2323 - A02 * A1323 + A03 * A1223),
            determinant * (A01 * A2313 - A02 * A1313 + A03 * A1213),
            determinant * - (A01 * A2312 - A02 * A1312 + A03 * A1212),
            determinant * - (A10 * A2323 - A12 * A0323 + A13 * A0223),
            determinant * (A00 * A2323 - A02 * A0323 + A03 * A0223),
            determinant * - (A00 * A2313 - A02 * A0313 + A03 * A0213),
            determinant * (A00 * A2312 - A02 * A0312 + A03 * A0212),
            determinant * (A10 * A1323 - A11 * A0323 + A13 * A0123),
            determinant * - (A00 * A1323 - A01 * A0323 + A03 * A0123),
            determinant * (A00 * A1313 - A01 * A0313 + A03 * A0113),
            determinant * - (A00 * A1312 - A01 * A0312 + A03 * A0112),
            determinant * - (A10 * A1223 - A11 * A0223 + A12 * A0123),
            determinant * (A00 * A1223 - A01 * A0223 + A02 * A0123),
            determinant * - (A00 * A1213 - A01 * A0213 + A02 * A0113),
            determinant * (A00 * A1212 - A01 * A0212 + A02 * A0112)]


cpdef list MatrixMultiplyMatrix(
        float A00, float A01, float A02, float A03,
        float A10, float A11, float A12, float A13,
        float A20, float A21, float A22, float A23,
        float A30, float A31, float A32, float A33,

        float B00, float B01, float B02, float B03,
        float B10, float B11, float B12, float B13,
        float B20, float B21, float B22, float B23,
        float B30, float B31, float B32, float B33):
    return [A00 * B00 + A01 * B10 + A02 * B20 + A03 * B30,
            A00 * B01 + A01 * B11 + A02 * B21 + A03 * B31,
            A00 * B02 + A01 * B12 + A02 * B22 + A03 * B32,
            A00 * B03 + A01 * B13 + A02 * B23 + A03 * B33,
            A10 * B00 + A11 * B10 + A12 * B20 + A13 * B30,
            A10 * B01 + A11 * B11 + A12 * B21 + A13 * B31,
            A10 * B02 + A11 * B12 + A12 * B22 + A13 * B32,
            A10 * B03 + A11 * B13 + A12 * B23 + A13 * B33,
            A20 * B00 + A21 * B10 + A22 * B20 + A23 * B30,
            A20 * B01 + A21 * B11 + A22 * B21 + A23 * B31,
            A20 * B02 + A21 * B12 + A22 * B22 + A23 * B32,
            A20 * B03 + A21 * B13 + A22 * B23 + A23 * B33,
            A30 * B00 + A31 * B10 + A32 * B20 + A33 * B30,
            A30 * B01 + A31 * B11 + A32 * B21 + A33 * B31,
            A30 * B02 + A31 * B12 + A32 * B22 + A33 * B32,
            A30 * B03 + A31 * B13 + A32 * B23 + A33 * B33]


cpdef list MatrixMultiplyVector(
        float A00, float A01, float A02, float A03,
        float A10, float A11, float A12, float A13,
        float A20, float A21, float A22, float A23,
        float A30, float A31, float A32, float A33,

        float Vx, float Vy, float Vz, float Vw):
    return [A00 * Vx + A01 * Vy + A02 * Vz + A03 * Vw,
            A10 * Vx + A11 * Vy + A12 * Vz + A13 * Vw,
            A20 * Vx + A21 * Vy + A22 * Vz + A23 * Vw,
            A30 * Vx + A31 * Vy + A32 * Vz + A33 * Vw]


cpdef list MatrixMultiplyVectors(
        float A00, float A01, float A02, float A03,
        float A10, float A11, float A12, float A13,
        float A20, float A21, float A22, float A23,
        float A30, float A31, float A32, float A33,
        list InputVectors):
    cdef list OutputVectors = list()
    cdef int i
    for i in range(len(InputVectors)):
        OutputVectors.append(
            Vector4(*MatrixMultiplyVector(
                A00, A01, A02, A03,
                A10, A11, A12, A13,
                A20, A21, A22, A23,
                A30, A31, A32, A33,
                *InputVectors[i].vector()))
        )
    return OutputVectors


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cdef void rasterizeTexturedTriangle2D(
        float[:, :] depthBuffer,
        surface_type screenBuffer,
        surface_type textureBuffer,
        float x1, float y1, float z1, float u1, float v1,
        float x2, float y2, float z2, float u2, float v2,
        float x3, float y3, float z3, float u3, float v3,
) nogil:
    cdef int screenWidth = screenBuffer.shape[1]
    cdef int screenHeight = screenBuffer.shape[0]
    cdef int textureWidth = textureBuffer.shape[1]
    cdef int textureHeight = textureBuffer.shape[0]

    x1 = max(min(x1, screenWidth), 0)
    x2 = max(min(x2, screenWidth), 0)
    x3 = max(min(x3, screenWidth), 0)

    y1 = max(min(y1, screenHeight), 0)
    y2 = max(min(y2, screenHeight), 0)
    y3 = max(min(y3, screenHeight), 0)

    cdef int maxX = int(max(x1, x2, x3))
    cdef int minX = int(min(x1, x2, x3))
    cdef int maxY = int(max(y1, y2, y3))
    cdef int minY = int(min(y1, y2, y3))

    cdef float area = (x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)
    cdef float dx1, dx2, dx3
    cdef float dy1, dy2, dy3
    cdef float W1, W2, W3
    cdef float w1, w2, w3, z
    cdef int x, y, u, v

    if area != 0 and z1 != 0 and z2 != 0 and z3 != 0:
        z1 = 1 / z1 / area
        z2 = 1 / z2 / area
        z3 = 1 / z3 / area

        u1 = u1 * z1 * textureWidth
        u2 = u2 * z2 * textureWidth
        u3 = u3 * z3 * textureWidth

        v1 = v1 * z1 * textureHeight
        v2 = v2 * z2 * textureHeight
        v3 = v3 * z3 * textureHeight

        dx1 = x2 - x3
        dx2 = x3 - x1
        dx3 = x1 - x2

        dy1 = y3 - y2
        dy2 = y1 - y3
        dy3 = y2 - y1

        W1 = (minX - x2) * (y3 - y2) - (minY - y2) * (x3 - x2)
        W2 = (minX - x3) * (y1 - y3) - (minY - y3) * (x1 - x3)
        W3 = (minX - x1) * (y2 - y1) - (minY - y1) * (x2 - x1)

        for y in range(minY, maxY):
            w1 = W1
            w2 = W2
            w3 = W3
            for x in range(minX, maxX):
                if w1 < 0 and w2 < 0 and w3 < 0:
                    z = w1 * z1 + w2 * z2 + w3 * z3
                    if depthBuffer[y][x] < z:
                        depthBuffer[y][x] = z
                        u = int((w1 * u1 + w2 * u2 + w3 * u3) / z)
                        v = int((w1 * v1 + w2 * v2 + w3 * v3) / z)
                        u = max(min(u, textureWidth), 0)
                        v = max(min(v, textureHeight), 0)
                        screenBuffer[y][x] = textureBuffer[v][u]
                w1 += dy1
                w2 += dy2
                w3 += dy3
            W1 += dx1
            W2 += dx2
            W3 += dx3


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cdef void rasterizeTexturedTriangle3D(
        float M00, float M01, float M02, float M03,
        float M10, float M11, float M12, float M13,
        float M20, float M21, float M22, float M23,
        float M30, float M31, float M32, float M33,

        float C00, float C01, float C02, float C03,
        float C10, float C11, float C12, float C13,
        float C20, float C21, float C22, float C23,
        float C30, float C31, float C32, float C33,

        float P00, float P01, float P02, float P03,
        float P10, float P11, float P12, float P13,
        float P20, float P21, float P22, float P23,
        float P30, float P31, float P32, float P33,

        float S00, float S01, float S02, float S03,
        float S10, float S11, float S12, float S13,
        float S20, float S21, float S22, float S23,
        float S30, float S31, float S32, float S33,

        float Cx, float Cy, float Cz,
        float[:, :] depthBuffer,
        surface_type screenBuffer,
        surface_type textureBuffer,
        float[:] triangle) nogil:

    cdef float x1 = triangle[0]
    cdef float y1 = triangle[1]
    cdef float z1 = triangle[2]
    cdef float w1 = triangle[3]
    cdef float u1 = triangle[4]
    cdef float v1 = triangle[5]

    cdef float x2 = triangle[6]
    cdef float y2 = triangle[7]
    cdef float z2 = triangle[8]
    cdef float w2 = triangle[9]
    cdef float u2 = triangle[10]
    cdef float v2 = triangle[11]

    cdef float x3 = triangle[12]
    cdef float y3 = triangle[13]
    cdef float z3 = triangle[14]
    cdef float w3 = triangle[15]
    cdef float u3 = triangle[16]
    cdef float v3 = triangle[17]

    cdef float mx1, my1, mz1, mw1
    cdef float mx2, my2, mz2, mw2
    cdef float mx3, my3, mz3, mw3
    cdef float mx4, my4, mz4, mw4

    cdef float cx1, cy1, cz1, cw1
    cdef float cx2, cy2, cz2, cw2
    cdef float cx3, cy3, cz3, cw3
    cdef float cx4, cy4, cz4, cw4

    cdef float px1, py1, pz1, pw1
    cdef float px2, py2, pz2, pw2
    cdef float px3, py3, pz3, pw3
    cdef float px4, py4, pz4, pw4

    cdef float sx1, sy1, sz1, sw1
    cdef float sx2, sy2, sz2, sw2
    cdef float sx3, sy3, sz3, sw3
    cdef float sx4, sy4, sz4, sw4

    mx1 = M00 * x1 + M01 * y1 + M02 * z1 + M03 * w1
    my1 = M10 * x1 + M11 * y1 + M12 * z1 + M13 * w1
    mz1 = M20 * x1 + M21 * y1 + M22 * z1 + M23 * w1
    mw1 = M30 * x1 + M31 * y1 + M32 * z1 + M33 * w1

    mx2 = M00 * x2 + M01 * y2 + M02 * z2 + M03 * w2
    my2 = M10 * x2 + M11 * y2 + M12 * z2 + M13 * w2
    mz2 = M20 * x2 + M21 * y2 + M22 * z2 + M23 * w2
    mw2 = M30 * x2 + M31 * y2 + M32 * z2 + M33 * w2

    mx3 = M00 * x3 + M01 * y3 + M02 * z3 + M03 * w3
    my3 = M10 * x3 + M11 * y3 + M12 * z3 + M13 * w3
    mz3 = M20 * x3 + M21 * y3 + M22 * z3 + M23 * w3
    mw3 = M30 * x3 + M31 * y3 + M32 * z3 + M33 * w3

    cdef float dx21, dy21, dz21
    cdef float dx31, dy31, dz31
    cdef float nx, ny, nz;

    dx21 = mx2 - mx1
    dy21 = my2 - my1
    dz21 = mz2 - mz1

    dx31 = mx3 - mx1
    dy31 = my3 - my1
    dz31 = mz3 - mz1
    nx = dy21 * dz31 - dz21 * dy31
    ny = dz21 * dx31 - dx21 * dz31
    nz = dx21 * dy31 - dy21 * dx31

    if (mx1 - Cx) * nx + (my1 - Cy) * ny + (mz1 - Cz) * nz < 0:
        cx1 = C00 * mx1 + C01 * my1 + C02 * mz1 + C03 * mw1
        cy1 = C10 * mx1 + C11 * my1 + C12 * mz1 + C13 * mw1
        cz1 = C20 * mx1 + C21 * my1 + C22 * mz1 + C23 * mw1
        cw1 = C30 * mx1 + C31 * my1 + C32 * mz1 + C33 * mw1

        cx2 = C00 * mx2 + C01 * my2 + C02 * mz2 + C03 * mw2
        cy2 = C10 * mx2 + C11 * my2 + C12 * mz2 + C13 * mw2
        cz2 = C20 * mx2 + C21 * my2 + C22 * mz2 + C23 * mw2
        cw2 = C30 * mx2 + C31 * my2 + C32 * mz2 + C33 * mw2

        cx3 = C00 * mx3 + C01 * my3 + C02 * mz3 + C03 * mw3
        cy3 = C10 * mx3 + C11 * my3 + C12 * mz3 + C13 * mw3
        cz3 = C20 * mx3 + C21 * my3 + C22 * mz3 + C23 * mw3
        cw3 = C30 * mx3 + C31 * my3 + C32 * mz3 + C33 * mw3


        px1 = P00 * cx1 + P01 * cy1 + P02 * cz1 + P03 * cw1
        py1 = P10 * cx1 + P11 * cy1 + P12 * cz1 + P13 * cw1
        pz1 = P20 * cx1 + P21 * cy1 + P22 * cz1 + P23 * cw1
        pw1 = P30 * cx1 + P31 * cy1 + P32 * cz1 + P33 * cw1

        px2 = P00 * cx2 + P01 * cy2 + P02 * cz2 + P03 * cw2
        py2 = P10 * cx2 + P11 * cy2 + P12 * cz2 + P13 * cw2
        pz2 = P20 * cx2 + P21 * cy2 + P22 * cz2 + P23 * cw2
        pw2 = P30 * cx2 + P31 * cy2 + P32 * cz2 + P33 * cw2

        px3 = P00 * cx3 + P01 * cy3 + P02 * cz3 + P03 * cw3
        py3 = P10 * cx3 + P11 * cy3 + P12 * cz3 + P13 * cw3
        pz3 = P20 * cx3 + P21 * cy3 + P22 * cz3 + P23 * cw3
        pw3 = P30 * cx3 + P31 * cy3 + P32 * cz3 + P33 * cw3


        sx1 = S00 * px1 + S01 * py1 + S02 * pz1 + S03 * pw1
        sy1 = S10 * px1 + S11 * py1 + S12 * pz1 + S13 * pw1
        sz1 = S20 * px1 + S21 * py1 + S22 * pz1 + S23 * pw1
        sw1 = S30 * px1 + S31 * py1 + S32 * pz1 + S33 * pw1

        sx2 = S00 * px2 + S01 * py2 + S02 * pz2 + S03 * pw2
        sy2 = S10 * px2 + S11 * py2 + S12 * pz2 + S13 * pw2
        sz2 = S20 * px2 + S21 * py2 + S22 * pz2 + S23 * pw2
        sw2 = S30 * px2 + S31 * py2 + S32 * pz2 + S33 * pw2

        sx3 = S00 * px3 + S01 * py3 + S02 * pz3 + S03 * pw3
        sy3 = S10 * px3 + S11 * py3 + S12 * pz3 + S13 * pw3
        sz3 = S20 * px3 + S21 * py3 + S22 * pz3 + S23 * pw3
        sw3 = S30 * px3 + S31 * py3 + S32 * pz3 + S33 * pw3

        rasterizeTexturedTriangle2D(
            depthBuffer,
            screenBuffer,
            textureBuffer,
            sx1 / sw1, sy1 / sw1, sw1, u1, v1,
            sx2 / sw2, sy2 / sw2, sw2, u2, v2,
            sx3 / sw3, sy3 / sw3, sw3, u3, v3)



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cpdef void rasterizeTexturedTriangles3D(
        float M00, float M01, float M02, float M03,
        float M10, float M11, float M12, float M13,
        float M20, float M21, float M22, float M23,
        float M30, float M31, float M32, float M33,

        float C00, float C01, float C02, float C03,
        float C10, float C11, float C12, float C13,
        float C20, float C21, float C22, float C23,
        float C30, float C31, float C32, float C33,

        float P00, float P01, float P02, float P03,
        float P10, float P11, float P12, float P13,
        float P20, float P21, float P22, float P23,
        float P30, float P31, float P32, float P33,

        float S00, float S01, float S02, float S03,
        float S10, float S11, float S12, float S13,
        float S20, float S21, float S22, float S23,
        float S30, float S31, float S32, float S33,

        float Cx, float Cy, float Cz,
        float[:, :] depthBuffer,
        surface_type screenBuffer,
        surface_type textureBuffer,
        float[:, :] triangles) nogil:

    cdef int i;
    for i in range(0, len(triangles)):
        rasterizeTexturedTriangle3D(
            M00, M01, M02, M03,
            M10, M11, M12, M13,
            M20, M21, M22, M23,
            M30, M31, M32, M33,

            C00, C01, C02, C03,
            C10, C11, C12, C13,
            C20, C21, C22, C23,
            C30, C31, C32, C33,

            P00, P01, P02, P03,
            P10, P11, P12, P13,
            P20, P21, P22, P23,
            P30, P31, P32, P33,

            S00, S01, S02, S03,
            S10, S11, S12, S13,
            S20, S21, S22, S23,
            S30, S31, S32, S33,

            Cx, Cy, Cz,
            depthBuffer,
            screenBuffer,
            textureBuffer,
            triangles[i]
        )
