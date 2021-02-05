class StringVector4:
    def __init__(self, x, y, z, w='1'):
        self.x, self.y, self.z, self.w = x, y, z, w

    def __str__(self):
        return f"{self.x}\n{self.y}\n{self.z}\n{self.w}"


class StringMatrix4x4:
    def __init__(self,
                 m00, m01, m02, m03,
                 m10, m11, m12, m13,
                 m20, m21, m22, m23,
                 m30, m31, m32, m33):
        self.m00, self.m01, self.m02, self.m03 = m00, m01, m02, m03
        self.m10, self.m11, self.m12, self.m13 = m10, m11, m12, m13
        self.m20, self.m21, self.m22, self.m23 = m20, m21, m22, m23
        self.m30, self.m31, self.m32, self.m33 = m30, m31, m32, m33

    def __matmul__(self, other):
        if isinstance(other, StringMatrix4x4):
            return StringMatrix4x4(
                f"({self.m00}) * ({other.m00}) + ({self.m01}) * ({other.m10}) + ({self.m02}) * ({other.m20}) + ({self.m03} * {other.m30})",
                f"({self.m00}) * ({other.m01}) + ({self.m01}) * ({other.m11}) + ({self.m02}) * ({other.m21}) + ({self.m03} * {other.m31})",
                f"({self.m00}) * ({other.m02}) + ({self.m01}) * ({other.m12}) + ({self.m02}) * ({other.m22}) + ({self.m03} * {other.m32})",
                f"({self.m00}) * ({other.m03}) + ({self.m01}) * ({other.m13}) + ({self.m02}) * ({other.m23}) + ({self.m03} * {other.m33})",
                f"({self.m10}) * ({other.m00}) + ({self.m11}) * ({other.m10}) + ({self.m12}) * ({other.m20}) + ({self.m13} * {other.m30})",
                f"({self.m10}) * ({other.m01}) + ({self.m11}) * ({other.m11}) + ({self.m12}) * ({other.m21}) + ({self.m13} * {other.m31})",
                f"({self.m10}) * ({other.m02}) + ({self.m11}) * ({other.m12}) + ({self.m12}) * ({other.m22}) + ({self.m13} * {other.m32})",
                f"({self.m10}) * ({other.m03}) + ({self.m11}) * ({other.m13}) + ({self.m12}) * ({other.m23}) + ({self.m13} * {other.m33})",
                f"({self.m20}) * ({other.m00}) + ({self.m21}) * ({other.m10}) + ({self.m22}) * ({other.m20}) + ({self.m23} * {other.m30})",
                f"({self.m20}) * ({other.m01}) + ({self.m21}) * ({other.m11}) + ({self.m22}) * ({other.m21}) + ({self.m23} * {other.m31})",
                f"({self.m20}) * ({other.m02}) + ({self.m21}) * ({other.m12}) + ({self.m22}) * ({other.m22}) + ({self.m23} * {other.m32})",
                f"({self.m20}) * ({other.m03}) + ({self.m21}) * ({other.m13}) + ({self.m22}) * ({other.m23}) + ({self.m23} * {other.m33})",
                f"({self.m30}) * ({other.m00}) + ({self.m31}) * ({other.m10}) + ({self.m32}) * ({other.m20}) + ({self.m33} * {other.m30})",
                f"({self.m30}) * ({other.m01}) + ({self.m31}) * ({other.m11}) + ({self.m32}) * ({other.m21}) + ({self.m33} * {other.m31})",
                f"({self.m30}) * ({other.m02}) + ({self.m31}) * ({other.m12}) + ({self.m32}) * ({other.m22}) + ({self.m33} * {other.m32})",
                f"({self.m30}) * ({other.m03}) + ({self.m31}) * ({other.m13}) + ({self.m32}) * ({other.m23}) + ({self.m33} * {other.m33})")
        elif isinstance(other, StringVector4):
            return StringVector4(
                f"({self.m00}) * ({other.x}) + ({self.m01}) * ({other.y}) + ({self.m02}) * ({other.z}) + ({self.m03}) * ({other.w})",
                f"({self.m10}) * ({other.x}) + ({self.m11}) * ({other.y}) + ({self.m12}) * ({other.z}) + ({self.m13}) * ({other.w})",
                f"({self.m20}) * ({other.x}) + ({self.m21}) * ({other.y}) + ({self.m22}) * ({other.z}) + ({self.m23}) * ({other.w})",
                f"({self.m30}) * ({other.x}) + ({self.m31}) * ({other.y}) + ({self.m32}) * ({other.z}) + ({self.m33}) * ({other.w})")

    def __str__(self):
        return f'''
{self.m00} {self.m01} {self.m02} {self.m03}
{self.m10} {self.m11} {self.m12} {self.m13}
{self.m20} {self.m21} {self.m22} {self.m23}
{self.m30} {self.m31} {self.m32} {self.m33}
        '''


model = StringMatrix4x4(
    'M00', 'M01', 'M02', 'M03',
    'M10', 'M11', 'M12', 'M13',
    'M20', 'M21', 'M22', 'M23',
    'M30', 'M31', 'M32', 'M33',
)
camera = StringMatrix4x4(
    'C00', 'C01', 'C02', 'C03',
    'C10', 'C11', 'C12', 'C13',
    'C20', 'C21', 'C22', 'C23',
    'C30', 'C31', 'C32', 'C33'
)

projection = StringMatrix4x4(
    'P00', 'P01', 'P02', 'P03',
    'P10', 'P11', 'P12', 'P13',
    'P20', 'P21', 'P22', 'P23',
    'P30', 'P31', 'P32', 'P33'
)

screen = StringMatrix4x4(
    'S00', 'S01', 'S02', 'S03',
    'S10', 'S11', 'S12', 'S13',
    'S20', 'S21', 'S22', 'S23',
    'S30', 'S31', 'S32', 'S33'
)

text = '''
block00 = (C00*(M00*x3 + M01*y3 + M02*z3 + M03*w3) +
               C01*(M10*x3 + M11*y3 + M12*z3 + M13*w3) +
               C02*(M20*x3 + M21*y3 + M22*z3 + M23*w3) +
               C03*(M30*x3 + M31*y3 + M32*z3 + M33*w3))
    block01 = (C10*(M00*x3 + M01*y3 + M02*z3 + M03*w3) +
               C11*(M10*x3 + M11*y3 + M12*z3 + M13*w3) +
               C12*(M20*x3 + M21*y3 + M22*z3 + M23*w3) +
               C13*(M30*x3 + M31*y3 + M32*z3 + M33*w3))
    block02 = (C20*(M00*x3 + M01*y3 + M02*z3 + M03*w3) +
               C21*(M10*x3 + M11*y3 + M12*z3 + M13*w3) +
               C22*(M20*x3 + M21*y3 + M22*z3 + M23*w3) +
               C23*(M30*x3 + M31*y3 + M32*z3 + M33*w3))
    block03 = (C30*(M00*x3 + M01*y3 + M02*z3 + M03*w3) +
               C31*(M10*x3 + M11*y3 + M12*z3 + M13*w3) +
               C32*(M20*x3 + M21*y3 + M22*z3 + M23*w3) +
               C33*(M30*x3 + M31*y3 + M32*z3 + M33*w3))
    block10 = P00*block00 + P01*block01 + P02*block02 + P03*block03
    block11 = P10*block00 + P11*block01 + P12*block02 + P13*block03
    block12 = P20*block00 + P21*block01 + P22*block02 + P23*block03
    block13 = P30*block00 + P31*block01 + P32*block02 + P33*block03
    
    x3 = S00*block10 + S01*block11 + S02*block12 + S03*block13
    y3 = S10*block10 + S11*block11 + S12*block12 + S13*block13
    z3 = S20*block10 + S21*block11 + S22*block12 + S23*block13
    w3 = S30*block10 + S31*block11 + S32*block12 + S33*block13
'''

text = text.replace("x3", "x2")
text = text.replace("y3", "y2")
text = text.replace("z3", "z2")
text = text.replace("w3", "w2")
print(text)


vector = StringVector4("x3", "y3", "z3", "w3")
vector = model @ vector
vector = camera @ vector
vector = projection @ vector
vector = screen @ vector

import sympy as sp

x3, y3, z3, w3 = sp.symbols('x3, y3, z3, w3', real=True)

M00, M01, M02, M03 = sp.symbols('M00, M01, M02, M03', real=True)
M10, M11, M12, M13 = sp.symbols('M10, M11, M12, M13', real=True)
M20, M21, M22, M23 = sp.symbols('M20, M21, M22, M23', real=True)
M30, M31, M32, M33 = sp.symbols('M30, M31, M32, M33', real=True)

C00, C01, C02, C03 = sp.symbols('C00, C01, C02, C03', real=True)
C10, C11, C12, C13 = sp.symbols('C10, C11, C12, C13', real=True)
C20, C21, C22, C23 = sp.symbols('C20, C21, C22, C23', real=True)
C30, C31, C32, C33 = sp.symbols('C30, C31, C32, C33', real=True)

P00, P01, P02, P03 = sp.symbols('P00, P01, P02, P03', real=True)
P10, P11, P12, P13 = sp.symbols('P10, P11, P12, P13', real=True)
P20, P21, P22, P23 = sp.symbols('P20, P21, P22, P23', real=True)
P30, P31, P32, P33 = sp.symbols('P30, P31, P32, P33', real=True)

S00, S01, S02, S03 = sp.symbols('S00, S01, S02, S03', real=True)
S10, S11, S12, S13 = sp.symbols('S10, S11, S12, S13', real=True)
S20, S21, S22, S23 = sp.symbols('S20, S21, S22, S23', real=True)
S30, S31, S32, S33 = sp.symbols('S30, S31, S32, S33', real=True)

print(eval(f"sp.simplify({vector.x})"))
print(eval(f"sp.simplify({vector.y})"))
print(eval(f"sp.simplify({vector.z})"))
print(eval(f"sp.simplify({vector.w})"))
