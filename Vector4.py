class Vector4:
    x, y, z, w = None, None, None, None

    def __init__(self, x, y, z, w: float = 1):
        self.x, self.y, self.z, self.w = x, y, z, w

    def data(self):
        return self.x, self.y, self.z, self.w

    def coords(self):
        return self.x, self.y, self.z

    def __add__(self, other):
        if isinstance(other, Vector4):
            return Vector4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector4(self.x + other, self.y + other, self.z + other, self.w + other)

    def __sub__(self, other):
        if isinstance(other, Vector4):
            return Vector4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector4(self.x - other, self.y - other, self.z - other, self.w - other)

    def __mul__(self, other):
        if isinstance(other, Vector4):
            return Vector4(self.x * other.x, self.y * other.y, self.z * other.z, self.w * other.w)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector4(self.x * other, self.y * other, self.z * other, self.w * other)

    def __truediv__(self, other):
        if isinstance(other, Vector4):
            return Vector4(self.x / other.x, self.y / other.y, self.z / other.z, self.w / other.w)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector4(self.x / other, self.y / other, self.z / other, self.w / other)

    def __str__(self):
        return f"Vector4({self.x}, {self.y}, {self.z}, {self.w})"
