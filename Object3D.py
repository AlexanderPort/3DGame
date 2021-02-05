from Matrix4x4 import Matrix4x4
from Vector4 import Vector4
from Texture import Texture
import pygame as pg
import random
import numpy as np
from graphics.rasterization import (rasterizeTexturedTriangles3D)


def random_color():
    return (int(random.random() * 255),
            int(random.random() * 255),
            int(random.random() * 255))


class Object3D:
    def __init__(self, renderer, triangles=None, position=None, rotation=None, scale=None):
        self.renderer = renderer
        self.texture = None

        if triangles is None: self.triangles = []
        else: self.triangles = triangles
        if position is None: self.position = Vector4(0, 0, 0)
        else: self.position = position
        if rotation is None: self.rotation = Vector4(0, 0, 0)
        else: self.rotation = rotation
        if scale is None: self.scale = Vector4(1, 1, 1)
        else: self.scale = scale
        self.direction = Vector4(0, 0, 0)

    def draw(self):
        self.position += self.direction
        if self.texture is not None:
            rasterizeTexturedTriangles3D(
                *self.getModelMatrix().data(),
                *self.renderer.CameraMatrix.data(),
                *self.renderer.ProjectionMatrix.data(),
                *self.renderer.ScreenMatrix.data(),
                *self.renderer.camera.position.coords(),
                self.renderer.depthBuffer,
                self.renderer.screenBuffer,
                self.renderer.textureBuffer[self.texture],
                self.triangles)

            '''
            rasterizeTexturedTriangles3D(*ModelMatrix.matrix(),
                                         *CAMERA_MATRIX[0].matrix(),
                                         *PROJECTION_MATRIX[0].matrix(),
                                         *SCREEN_MATRIX[0].matrix(),
                                         DEPTH_BUFFER,
                                         SCREEN_BUFFER,
                                         TEXTURE_BUFFER[0][self.texture],
                                         self.triangles)
            '''
        else:
            vertexes = self.renderer.camera_matrix @ self.vertexes
            vertexes = self.renderer.projection_matrix @ vertexes
            vertexes = self.renderer.to_screen_matrix @ vertexes

            for index in self.indexes:
                vertex1 = vertexes[index[0]]
                vertex2 = vertexes[index[1]]
                vertex3 = vertexes[index[2]]

                triangle = [
                    [vertex1.x / vertex1.w, vertex1.y / vertex1.w],
                    [vertex2.x / vertex2.w, vertex2.y / vertex2.w],
                    [vertex3.x / vertex3.w, vertex3.y / vertex3.w],
                ]

                color = random_color()
                if self.renderer.fill:
                    pg.draw.polygon(self.renderer.screen, color, triangle)
                pg.draw.polygon(self.renderer.screen, color, triangle, 1)

        '''
        if self.texture is not None:
            ModelMatrix = self.getModelMatrix()
            rasterizeTexturedTriangles3D(*ModelMatrix.matrix(),
                                         *CAMERA_MATRIX[0].matrix(),
                                         *PROJECTION_MATRIX[0].matrix(),
                                         *SCREEN_MATRIX[0].matrix(),
                                         DEPTH_BUFFER[0],
                                         SCREEN_BUFFER[0],
                                         TEXTURE_BUFFER[0][self.texture],
                                         self.triangles)
        '''

        '''
        vertexes = self.renderer.camera_matrix @ self.vertexes
        vertexes = self.renderer.projection_matrix @ vertexes
        vertexes = self.renderer.to_screen_matrix @ vertexes

        for index in self.indexes:
            vertex1 = vertexes[index[0]]
            vertex2 = vertexes[index[1]]
            vertex3 = vertexes[index[2]]
            vertex4 = vertexes[index[3]]

            polygon = [
                [vertex1.x / vertex1.w, vertex1.y / vertex1.w],
                [vertex2.x / vertex2.w, vertex2.y / vertex2.w],
                [vertex3.x / vertex3.w, vertex3.y / vertex3.w],
                [vertex4.x / vertex4.w, vertex4.y / vertex4.w],
            ]

            color = random_color()
            if self.renderer.fill:
                pg.draw.polygon(self.renderer.screen, color, polygon)
            pg.draw.polygon(self.renderer.screen, color, polygon, 3)
        '''

    def getTranslationMatrix(self):
        return Matrix4x4.translate(self.position.x,
                                   self.position.y,
                                   self.position.z)

    def getRotationMatrix(self):
        rotate_x = Matrix4x4.rotate_x(self.rotation.x)
        rotate_y = Matrix4x4.rotate_y(self.rotation.y)
        rotate_z = Matrix4x4.rotate_z(self.rotation.z)
        return rotate_z @ rotate_y @ rotate_x

    def getScaleMatrix(self):
        return Matrix4x4.scale(self.scale.x,
                               self.scale.y,
                               self.scale.z)

    def getModelMatrix(self):
        return self.getTranslationMatrix() @ self.getRotationMatrix() @ self.getScaleMatrix()

    def loadTexture(self, filename):
        self.texture = Texture(self.renderer, filename).filename

    def setPosition(self, x, y, z):
        self.position = Vector4(x, y, z)

    def setRotation(self, x, y, z):
        self.rotation = Vector4(x, y, z)

    def setScale(self, x, y, z):
        self.scale = Vector4(x, y, z)

    @staticmethod
    def loadObjectModel(renderer, path):
        with open(path, mode='r', encoding='utf-8') as file:
            faceVertexes, faceIndexes = [], []
            textureVertexes, textureIndexes = [], []
            for line in file.readlines():
                if line.startswith('v '):
                    x, y, z = map(float, line.split()[1:])
                    faceVertexes.append([x, y, z, 1])
                elif line.startswith('vt'):
                    u, v = list(map(float, line.split()[1:]))[:2]
                    textureVertexes.append([u, v])
                elif line.startswith('f '):
                    line = line.split()[1:]
                    faceIndex, textureIndex, normalIndex = [], [], []
                    for i in range(len(line)):
                        indexes = list(map(int, line[i].split('/')))
                        if len(indexes) == 2:
                            f, t = indexes
                            faceIndex.append(f - 1)
                            textureIndex.append(t - 1)
                        elif len(indexes) == 3:
                            f, t, n = indexes
                            faceIndex.append(f - 1)
                            textureIndex.append(t - 1)
                            normalIndex.append(n - 1)
                    faceIndexes.append(faceIndex)
                    textureIndexes.append(textureIndex)
            triangles = []
            if len(textureIndexes) > 0:
                for i in range(len(faceIndexes)):
                    faceIndex = faceIndexes[i]
                    textureIndex = textureIndexes[i]
                    for j in range(1, len(faceIndex) - 1):
                        triangles.append(
                            [*faceVertexes[faceIndex[0]], *textureVertexes[textureIndex[0]],
                             *faceVertexes[faceIndex[j]], *textureVertexes[textureIndex[j]],
                             *faceVertexes[faceIndex[j + 1]], *textureVertexes[textureIndex[j + 1]]]
                        )

            return Object3D(renderer, np.array(triangles, dtype=np.float32))
