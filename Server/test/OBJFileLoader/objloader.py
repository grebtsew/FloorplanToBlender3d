import os
import pygame
from OpenGL.GL import *


class OBJ:
    generate_on_init = True

    @classmethod
    def loadTexture(cls, imagefile):
        surf = pygame.image.load(imagefile)
        image = pygame.image.tostring(surf, "RGBA", 1)
        ix, iy = surf.get_rect().size
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image
        )
        return texid

    @classmethod
    def loadMaterial(cls, filename):
        contents = {}
        mtl = None
        dirname = os.path.dirname(filename)

        for line in open(filename, "r"):
            if line.startswith("#"):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == "newmtl":
                mtl = contents[values[1]] = {}
            elif mtl is None:
                raise ValueError("mtl file doesn't start with newmtl stmt")
            elif values[0] == "map_Kd":
                # load the texture referred to by this declaration
                mtl[values[0]] = values[1]
                imagefile = os.path.join(dirname, mtl["map_Kd"])
                mtl["texture_Kd"] = cls.loadTexture(imagefile)
            else:
                mtl[values[0]] = list(map(float, values[1:]))
        return contents

    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file."""
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.gl_list = 0
        dirname = os.path.dirname(filename)

        material = None
        for line in open(filename, "r"):
            if line.startswith("#"):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == "v":
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == "vn":
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == "vt":
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ("usemtl", "usemat"):
                material = values[1]
            elif values[0] == "mtllib":
                self.mtl = self.loadMaterial(os.path.join(dirname, values[1]))
            elif values[0] == "f":
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split("/")
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
        if self.generate_on_init:
            self.generate()

    def generate(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            mtl = self.mtl[material]
            if "texture_Kd" in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl["texture_Kd"])
            else:
                # just use diffuse colour
                glColor(*mtl["Kd"])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

    def render(self):
        glCallList(self.gl_list)

    def free(self):
        glDeleteLists([self.gl_list])
