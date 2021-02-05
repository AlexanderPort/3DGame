from Matrix4x4 import Matrix4x4
from Vector4 import Vector4
import math
import pygame as pg


class Camera:
    def __init__(self, renderer, position: Vector4):
        self.position = position
        self.forward = Vector4(0, 0, 1)
        self.right = Vector4(1, 0, 0)
        self.up = Vector4(0, 1, 0)
        self.near_plane = 0.1
        self.far_plane = 1000
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (renderer.HEIGHT / renderer.WIDTH)
        self.moving_speed = 10
        self.rotation_speed = 1

    def translate_matrix(self):
        x, y, z = self.position.coords()
        return Matrix4x4(
            1, 0, 0, -x,
            0, 1, 0, -y,
            0, 0, 1, -z,
            0, 1, 0, 1)

    def rotate_matrix(self):
        fx, fy, fz = self.forward.coords()
        rx, ry, rz = self.right.coords()
        ux, uy, uz = self.up.coords()
        return Matrix4x4(
            rx, ry, rz, 0,
            ux, uy, uz, 0,
            fx, fy, fz, 0,
            0, 0, 0, 1)

    def CameraMatrix(self):
        return self.rotate_matrix() @ self.translate_matrix()

    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position += self.up * self.moving_speed
        if key[pg.K_d]:
            self.position -= self.up * self.moving_speed
        if key[pg.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pg.K_q]:
            self.position += self.right * self.moving_speed
        if key[pg.K_e]:
            self.position -= self.right * self.moving_speed

        if key[pg.K_LEFT]:
            self.camera_yaw(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_yaw(self.rotation_speed)
        if key[pg.K_UP]:
            self.camera_pitch(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_pitch(self.rotation_speed)

    def camera_yaw(self, angle):
        rotate = Matrix4x4.rotate_x(angle)
        self.forward = rotate @ self.forward
        self.right = rotate @ self.right
        self.up = rotate @ self.up

    def camera_pitch(self, angle):
        rotate = Matrix4x4.rotate_y(angle)
        self.forward = rotate @ self.forward
        self.right = rotate @ self.right
        self.up = rotate @ self.up

    def InverseCameraMatrix(self):
        return self.translate_matrix().inverse() @ self.rotate_matrix().inverse()
