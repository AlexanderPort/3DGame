import pygame as pg


class Texture:
    def __init__(self, renderer, filename):
        self.filename = filename
        self.renderer = renderer
        if filename not in renderer.textureBuffer:
            texture = pg.image.load(filename)
            self.texture = pg.Surface(texture.get_size(), depth=8)
            self.texture.blit(texture, (0, 0))
            self.renderer.textureBuffer[filename] = self.getBuffer()

    def getBuffer(self):
        return pg.surfarray.pixels2d(self.texture)