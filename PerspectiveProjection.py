import math
from Matrix4x4 import Matrix4x4


class PerspectiveProjection:
    def __init__(self, renderer):
        NEAR = renderer.camera.near_plane
        FAR = renderer.camera.far_plane
        RIGHT = math.tan(renderer.camera.h_fov / 2)
        LEFT = -RIGHT
        TOP = math.tan(renderer.camera.v_fov / 2)
        BOTTOM = -TOP

        self.m00 = 2 / (RIGHT - LEFT)
        self.m11 = 2 / (TOP - BOTTOM)
        self.m22 = (FAR + NEAR) / (FAR - NEAR)
        self.m32 = -2 * NEAR * FAR / (FAR - NEAR)
        self.ProjectionMatrix = Matrix4x4(
            self.m00, 0, 0, 0,
            0, self.m11, 0, 0,
            0, 0, self.m22, self.m32,
            0, 0, 1, 0)

        self.HW, self.HH = renderer.H_WIDTH, renderer.H_HEIGHT
        self.ScreenMatrix = Matrix4x4(
            self.HW, 0, 0, self.HW,
            0, -self.HH, 0, self.HH,
            0, 0, 1, 0,
            0, 0, 0, 1)
