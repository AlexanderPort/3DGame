import math
from Vector4 import Vector4
from graphics import (MatrixMultiplyMatrix,
                      MatrixMultiplyVector,
                      MatrixMultiplyVectors,
                      InverseMatrix)


class Matrix4x4:
    def __init__(self, matrix):
        self.matrix = matrix

    @staticmethod
    def zeros():
        return Matrix4x4([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])

    @staticmethod
    def identity():
        return Matrix4x4([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

    @staticmethod
    def scale(x, y, z):
        return Matrix4x4([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1],
        ])

    @staticmethod
    def translate(x, y, z):
        return Matrix4x4([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1],
        ])

    @staticmethod
    def rotate_x(angle):
        radians = math.radians(angle)
        sin = math.sin(radians)
        cos = math.cos(radians)
        return Matrix4x4([
            [1, 0, 0, 0],
            [0, cos, -sin, 0],
            [0, sin, cos, 0],
            [0, 0, 0, 1],
        ])

    @staticmethod
    def rotate_y(angle):
        radians = math.radians(angle)
        sin = math.sin(radians)
        cos = math.cos(radians)
        return Matrix4x4([
            [cos, 0, sin, 0],
            [0, 1, 0, 0],
            [-sin, 0, cos, 0],
            [0, 0, 0, 1],
        ])

    @staticmethod
    def rotate_z(angle):
        radians = math.radians(angle)
        sin = math.sin(radians)
        cos = math.cos(radians)
        return Matrix4x4([
            [cos, -sin, 0, 0],
            [sin, cos, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

    def __getitem__(self, item):
        return self.matrix[item]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def __matmul__(self, other):
        if isinstance(other, Matrix4x4):
            return Matrix4x4([
                [self.matrix[0][0] * other.matrix[0][0] + self.matrix[0][1] * other.matrix[1][0] + self.matrix[0][2] * other.matrix[2][0] + self.matrix[0][3] * other.matrix[3][0],
                 self.matrix[0][0] * other.matrix[0][1] + self.matrix[0][1] * other.matrix[1][1] + self.matrix[0][2] * other.matrix[2][1] + self.matrix[0][3] * other.matrix[3][1],
                 self.matrix[0][0] * other.matrix[0][2] + self.matrix[0][1] * other.matrix[1][2] + self.matrix[0][2] * other.matrix[2][2] + self.matrix[0][3] * other.matrix[3][2],
                 self.matrix[0][0] * other.matrix[0][3] + self.matrix[0][1] * other.matrix[1][3] + self.matrix[0][2] * other.matrix[2][3] + self.matrix[0][3] * other.matrix[3][3]],
                [self.matrix[1][0] * other.matrix[0][0] + self.matrix[1][1] * other.matrix[1][0] + self.matrix[1][2] * other.matrix[2][0] + self.matrix[1][3] * other.matrix[3][0],
                 self.matrix[1][0] * other.matrix[0][1] + self.matrix[1][1] * other.matrix[1][1] + self.matrix[1][2] * other.matrix[2][1] + self.matrix[1][3] * other.matrix[3][1],
                 self.matrix[1][0] * other.matrix[0][2] + self.matrix[1][1] * other.matrix[1][2] + self.matrix[1][2] * other.matrix[2][2] + self.matrix[1][3] * other.matrix[3][2],
                 self.matrix[1][0] * other.matrix[0][3] + self.matrix[1][1] * other.matrix[1][3] + self.matrix[1][2] * other.matrix[2][3] + self.matrix[1][3] * other.matrix[3][3]],
                [self.matrix[2][0] * other.matrix[0][0] + self.matrix[2][1] * other.matrix[1][0] + self.matrix[2][2] * other.matrix[2][0] + self.matrix[2][3] * other.matrix[3][0],
                 self.matrix[2][0] * other.matrix[0][1] + self.matrix[2][1] * other.matrix[1][1] + self.matrix[2][2] * other.matrix[2][1] + self.matrix[2][3] * other.matrix[3][1],
                 self.matrix[2][0] * other.matrix[0][2] + self.matrix[2][1] * other.matrix[1][2] + self.matrix[2][2] * other.matrix[2][2] + self.matrix[2][3] * other.matrix[3][2],
                 self.matrix[2][0] * other.matrix[0][3] + self.matrix[2][1] * other.matrix[1][3] + self.matrix[2][2] * other.matrix[2][3] + self.matrix[2][3] * other.matrix[3][3]],
                [self.matrix[3][0] * other.matrix[0][0] + self.matrix[3][1] * other.matrix[1][0] + self.matrix[3][2] * other.matrix[2][0] + self.matrix[3][3] * other.matrix[3][0],
                 self.matrix[3][0] * other.matrix[0][1] + self.matrix[3][1] * other.matrix[1][1] + self.matrix[3][2] * other.matrix[2][1] + self.matrix[3][3] * other.matrix[3][1],
                 self.matrix[3][0] * other.matrix[0][2] + self.matrix[3][1] * other.matrix[1][2] + self.matrix[3][2] * other.matrix[2][2] + self.matrix[3][3] * other.matrix[3][2],
                 self.matrix[3][0] * other.matrix[0][3] + self.matrix[3][1] * other.matrix[1][3] + self.matrix[3][2] * other.matrix[2][3] + self.matrix[3][3] * other.matrix[3][3]]
            ])
        elif isinstance(other, Vector4):
            return Vector4(
                self.matrix[0][0] * other.x + self.matrix[0][1] * other.y + self.matrix[0][2] * other.z + self.matrix[0][3] * other.w,
                self.matrix[1][0] * other.x + self.matrix[1][1] * other.y + self.matrix[1][2] * other.z + self.matrix[1][3] * other.w,
                self.matrix[2][0] * other.x + self.matrix[2][1] * other.y + self.matrix[2][2] * other.z + self.matrix[2][3] * other.w,
                self.matrix[3][0] * other.x + self.matrix[3][1] * other.y + self.matrix[3][2] * other.z + self.matrix[3][3] * other.w,
            )
        elif isinstance(other, list):
            result = []
            for i in range(len(other)):
                result.append(self @ other[i])
            return result

    def __str__(self):
        return f'''
{self.matrix[0][0]} {self.matrix[0][1]} {self.matrix[0][2]} {self.matrix[0][3]}
{self.matrix[1][0]} {self.matrix[1][1]} {self.matrix[1][2]} {self.matrix[1][3]}
{self.matrix[2][0]} {self.matrix[2][1]} {self.matrix[2][2]} {self.matrix[2][3]}
{self.matrix[3][0]} {self.matrix[3][1]} {self.matrix[3][2]} {self.matrix[3][3]}
        '''

    @property
    def T(self):
        return Matrix4x4([
            [self.matrix[0][0], self.matrix[1][0], self.matrix[2][0], self.matrix[3][0]],
            [self.matrix[0][1], self.matrix[1][1], self.matrix[2][1], self.matrix[3][1]],
            [self.matrix[0][2], self.matrix[1][2], self.matrix[2][2], self.matrix[3][2]],
            [self.matrix[0][3], self.matrix[1][3], self.matrix[2][3], self.matrix[3][3]],
        ])


class FastMatrix4x4:
    def __init__(self,
                 m00, m01, m02, m03,
                 m10, m11, m12, m13,
                 m20, m21, m22, m23,
                 m30, m31, m32, m33):
        self.m00, self.m01, self.m02, self.m03 = m00, m01, m02, m03
        self.m10, self.m11, self.m12, self.m13 = m10, m11, m12, m13
        self.m20, self.m21, self.m22, self.m23 = m20, m21, m22, m23
        self.m30, self.m31, self.m32, self.m33 = m30, m31, m32, m33

    @staticmethod
    def zeros():
        return FastMatrix4x4(
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0
        )

    @staticmethod
    def identity():
        return FastMatrix4x4(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1,
        )

    @staticmethod
    def scale(x, y, z):
        return FastMatrix4x4(
            x, 0, 0, 0,
            0, y, 0, 0,
            0, 0, z, 0,
            0, 0, 0, 1,
        )

    @staticmethod
    def translate(x, y, z):
        return FastMatrix4x4(
            1, 0, 0, x,
            0, 1, 0, y,
            0, 0, 1, z,
            0, 0, 0, 1,
        )

    @staticmethod
    def rotate_x(angle):
        radians = math.radians(angle)
        sin = math.sin(radians)
        cos = math.cos(radians)
        return FastMatrix4x4(
            1, 0, 0, 0,
            0, cos, -sin, 0,
            0, sin, cos, 0,
            0, 0, 0, 1,
        )

    @staticmethod
    def rotate_y(angle):
        radians = math.radians(angle)
        sin = math.sin(radians)
        cos = math.cos(radians)
        return FastMatrix4x4(
            cos, 0, sin, 0,
            0, 1, 0, 0,
            -sin, 0, cos, 0,
            0, 0, 0, 1,
        )

    @staticmethod
    def rotate_z(angle):
        radians = math.radians(angle)
        sin = math.sin(radians)
        cos = math.cos(radians)
        return FastMatrix4x4(
            cos, -sin, 0, 0,
            sin, cos, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1,
        )

    def __matmul__(self, other):

        if isinstance(other, FastMatrix4x4):
            return FastMatrix4x4(*MatrixMultiplyMatrix(*self.data(), *other.data()))
        elif isinstance(other, Vector4):
            return Vector4(*MatrixMultiplyVector(*self.data(), *other.data()))
        elif isinstance(other, list):
            return MatrixMultiplyVectors(*self.data(), other)

    def data(self):
        return (self.m00, self.m01, self.m02, self.m03,
                self.m10, self.m11, self.m12, self.m13,
                self.m20, self.m21, self.m22, self.m23,
                self.m30, self.m31, self.m32, self.m33)

    def inverse(self):
        return FastMatrix4x4(*InverseMatrix(*self.data()))

    @property
    def T(self):
        return FastMatrix4x4(
            self.m00, self.m10, self.m20, self.m30,
            self.m01, self.m11, self.m21, self.m31,
            self.m02, self.m12, self.m22, self.m32,
            self.m03, self.m13, self.m23, self.m33)

    def __str__(self):
        return f'''
{self.m00} {self.m01} {self.m02} {self.m03}
{self.m10} {self.m11} {self.m12} {self.m13}
{self.m20} {self.m21} {self.m22} {self.m23}
{self.m30} {self.m31} {self.m32} {self.m33}
        '''


Matrix4x4 = FastMatrix4x4

