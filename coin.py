import math
import random
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
DEGREE_STEP = 10


def degrees_to_radians(degrees):
    return degrees * 0.0174532925


class Coin(object):
    def __init__(self):
        self.initial_x = random.random() * 10.0 - 5
        self.initial_z = random.random() * 10.0 - 5
        self.color = [random.random(), random.random(), random.random()]
        self.size = random.random() + 0.1
        self.y_offset = -50
        self.x_offset = random.random() * 30.0
        self.z_offset = random.random() * 30.0
        self.speed = random.random() * 0.5 + 0.1
        self.rotational_speed = random.random() * 5.0
        self.current_angle = 0

    def draw_one_sided_circle(self):
        glBegin(GL_POLYGON)
        for degrees in range(0, 360, DEGREE_STEP):
            t = degrees_to_radians(degrees)
            sin_val = math.sin(t)
            x = 10 * math.cos(t)
            y = 10 * math.sin(t)
            glVertex3f(x, y, -1.0)
        glEnd()

        prev_x = None
        prev_y = None
        for degrees in range(0, 360, DEGREE_STEP):
            t = degrees_to_radians(degrees)
            x = 10 * math.cos(t)
            y = 10 * math.sin(t)
            if prev_x is not None:
                glBegin(GL_POLYGON)
                glVertex3f(x, y, 1.0)
                glVertex3f(x, y, -1.0)
                glVertex3f(prev_x, prev_y, -1.0)
                glVertex3f(prev_x, prev_y, 1.0)
                glEnd()
            prev_x = x
            prev_y = y

    def draw(self):
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color)
        glPushMatrix()
        glTranslatef(self.x_offset, self.y_offset, self.z_offset)
        glPushMatrix()
        glScalef(self.size, self.size, self.size)
        glPushMatrix()
        glRotatef(self.current_angle, 0, 1, 0)

        glPushMatrix()
        self.draw_one_sided_circle()
        glPopMatrix()
        glPushMatrix()
        glRotatef(180.0, 0, 1, 0)
        self.draw_one_sided_circle()
        glPopMatrix()
        glPopMatrix()

        glPopMatrix()
        glPopMatrix()

    def tick(self):
        self.current_angle += self.rotational_speed
        self.y_offset += self.speed
