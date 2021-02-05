import pygame as pg
from Camera import Camera
from Matrix4x4 import Matrix4x4
from Vector4 import Vector4
from PerspectiveProjection import PerspectiveProjection
from Object3D import *
import random
from pygame.locals import *
import numpy as np
import ctypes
import math

pg.init()
pg.font.init()

# python setup.py build_ext --inplace


WHITE = (255, 255, 255)


class Renderer:
    def __init__(self):
        self.fps = 0
        self.frames = 0
        self.FPS = 60
        self.fill = False
        ctypes.windll.user32.SetProcessDPIAware()
        resolution = (ctypes.windll.user32.GetSystemMetrics(0),
                      ctypes.windll.user32.GetSystemMetrics(1))
        # resolution = (1000, 500)
        self.RESOLUTION = self.WIDTH, self.HEIGHT = resolution
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.display = pg.display.set_mode(self.RESOLUTION)
        self.screen = pg.Surface(self.RESOLUTION, depth=8)
        self.screen.set_alpha(None)
        self.clock = pg.time.Clock()
        self.depthBuffer = None
        self.screenBuffer = None
        self.textureBuffer = dict()

        self.camera = Camera(self, Vector4(0, 0, 0))
        self.projection = PerspectiveProjection(self)

        self.CameraMatrix = self.camera.CameraMatrix()
        self.ScreenMatrix = self.projection.ScreenMatrix
        self.ProjectionMatrix = self.projection.ProjectionMatrix

        self.objects = []

        for i in range(1):
            self.objects.append(Object3D.loadObjectModel(self, "models/planet.obj"))
            self.objects[i].setPosition(
                random.random() * 1000,
                random.random() * 1000,
                random.random() * 1000
            )
            self.objects[i].setScale(1, 1, 1)
            self.objects[i].loadTexture("textures/lava.jpg")

        self.sylvana = Object3D.loadObjectModel(self, "models/Sylvanas.obj")
        self.sylvana.loadTexture("textures/black.jpg")
        self.sylvana.setScale(100, 100, 100)
        self.sylvana.setRotation(0, 180, 0)
        self.objects.append(self.sylvana)
        self.num_triangles = 0

    def draw(self):
        self.num_triangles = 0
        for i in range(len(self.objects)):

            object3D = self.objects[i]
            object3D.rotation += 1
            self.num_triangles += len(object3D.triangles)
            '''
            dx = self.camera.position.x - object3D.position[0]
            dy = self.camera.position.y - object3D.position[1]
            dz = self.camera.position.z - object3D.position[2]
            length = math.sqrt(dx * dx + dy * dy + dz * dz)
            if length != 0:
                object3D.direction = [dx / length, dy / length, dz / length]
            '''
            object3D.draw()
            '''
            args = (object3D.getModelMatrix().matrix(),
                    self.CameraMatrix.matrix(),
                    self.ProjectionMatrix.matrix(),
                    self.ScreenMatrix.matrix(),
                    self.depthBuffer,
                    self.screenBuffer,
                    self.textureBuffer[object3D.texture],
                    object3D.triangles)
            process = Process(target=rasterizeTriangles, args=args)
            processes.append(process)
            process.start()
            '''

    def start(self):
        running = True
        font = pg.font.Font(None, 50)
        textures = ["space.jpg", "flowers.jpg", "lava.jpg", "ice.jpg", "stones.jpg"]
        while running:
            self.screen.fill((0, 0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.display = pg.display.set_mode((2000, 1500))
                        self.screen = pg.Surface((2000, 1500), depth=8)
                        self.projection = PerspectiveProjection(self)
                        self.ProjectionMatrix = self.projection.ProjectionMatrix
                        running = False
                    if event.key == pg.K_SPACE:
                        for i in range(1):
                            direction = Vector4(
                                2 * random.random() - 1,
                                2 * random.random() - 1,
                                2 * random.random() - 1,
                            )
                            object3D = Object3D.loadObjectModel(self, "models/cube.obj")
                            object3D.setScale(10, 10, 10)
                            object3D.setPosition(
                                self.camera.position.x,
                                self.camera.position.y,
                                self.camera.position.z + 100
                            )
                            object3D.direction = direction
                            texture = textures[random.randint(0, len(textures) - 1)]
                            object3D.loadTexture("textures/" + texture)
                            self.objects.append(object3D)

            self.CameraMatrix = self.camera.CameraMatrix()

            self.lockSurfaces()
            '''
            global CAMERA_MATRIX, PROJECTION_MATRIX, \
                SCREEN_MATRIX, DEPTH_BUFFER, \
                SCREEN_BUFFER, TEXTURE_BUFFER
            CAMERA_MATRIX[0] = self.CameraMatrix
            PROJECTION_MATRIX[0] = self.ProjectionMatrix
            SCREEN_MATRIX[0] = self.ScreenMatrix
            DEPTH_BUFFER[0] = self.depthBuffer
            SCREEN_BUFFER[0] = self.screenBuffer
            TEXTURE_BUFFER[0] = self.textureBuffer
            '''

            self.draw()
            self.unlockSurfaces()
            mouse = pg.mouse.get_pressed(3)
            pos = list(pg.mouse.get_pos())
            if mouse[0]:
                '''
                float imageAspectRatio = imageWidth / imageHeight; // assuming width > height 
float Px = (2 * ((x + 0.5) / imageWidth) - 1) * tan(fov / 2 * M_PI / 180) * imageAspectRatio; 
float Py = (1 - 2 * ((y + 0.5) / imageHeight) * tan(fov / 2 * M_PI / 180); 
Vec3f rayOrigin = Point3(0, 0, 0); 
Matrix44f cameraToWorld; 
cameraToWorld.set(...); // set matrix 
Vec3f rayOriginWorld, rayPWorld; 
cameraToWorld.multVectMatrix(rayOrigin, rayOriginWorld); 
cameraToWorld.multVectMatrix(Vec3f(Px, Py, -1), rayPWorld); 
Vec3f rayDirection = rayPWorld - rayOriginWorld; 
rayDirection.normalize();
                '''
                inverseMatrix = (self.CameraMatrix @ self.ProjectionMatrix).inverse()
                screenAspectRatio = self.WIDTH / self.HEIGHT
                tan = math.tan(self.camera.h_fov / 2)
                Px = (2 * (pos[0] + 0.5) / self.WIDTH - 1) * screenAspectRatio
                Py = (1 - 2 * (pos[1] + 0.5) / self.HEIGHT)
                point1 = self.camera.position
                point2 = inverseMatrix @ Vector4(pos[0], pos[1], -1)
                dx = point2.x - point1.x
                dy = point2.y - point1.y
                dz = point2.z - point1.z
                length = math.sqrt(dx * dx + dy * dy + dz * dz)
                for i in range(1):
                    direction = Vector4(
                        dx / length,
                        dy / length,
                        dz / length,
                        0
                    )
                    object3D = Object3D.loadObjectModel(self, "models/cube.obj")
                    object3D.setScale(10, 10, 10)
                    object3D.setPosition(
                        self.camera.position.x,
                        self.camera.position.y,
                        self.camera.position.z
                    )
                    object3D.direction = direction * 5
                    texture = textures[random.randint(0, len(textures) - 1)]
                    object3D.loadTexture("textures/" + texture)
                    self.objects.append(object3D)

            self.camera.control()
            self.display.blit(self.screen, (0, 0))
            fps_text = font.render(f"fps={self.fps}", True, WHITE)
            triangles_text = font.render(f"triangles={self.num_triangles}", True, WHITE)
            camera_position_x_text = font.render(f"x={self.camera.position.x}", True, WHITE)
            camera_position_y_text = font.render(f"y={self.camera.position.y}", True, WHITE)
            camera_position_z_text = font.render(f"z={self.camera.position.z}", True, WHITE)

            texts = [
                fps_text,
                camera_position_x_text,
                camera_position_y_text,
                camera_position_z_text,
                triangles_text
            ]

            for i in range(len(texts)):
                self.display.blit(texts[i], (0, i * font.get_height()))

            pg.display.flip()
            self.clock.tick(self.FPS)
            self.fps = self.clock.get_fps()

    def lockSurfaces(self):
        self.depthBuffer = np.zeros(self.RESOLUTION, dtype=np.float32)
        self.screenBuffer = pg.surfarray.pixels2d(self.screen)

    def unlockSurfaces(self):
        self.screen = pg.surfarray.make_surface(self.screenBuffer)



