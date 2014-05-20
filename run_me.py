from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


from coin import Coin

import random
import math

WIDTH = 1024
HEIGHT = 768
SCALAR = 60.0
TICK_INCR = 0.5


def degrees_to_radians(degrees):
    return degrees * 0.0174532925


class OpenGLExample(object):
    def __init__(self):
        self.ticks = 0.0
        self.all_drawable_objects = []

    def update_eye(self):
        # camera point
        # target point
        # up vector
        gluLookAt(SCALAR * math.cos(degrees_to_radians(self.ticks)),
                5.0,  # Z height
                SCALAR * math.sin(degrees_to_radians(self.ticks)),

                0.0,
                0.0,
                0.0,

                0.0,
                1.0,
                0.0)

    def key_pressed(self, key, x, y):
        if key == 'q' or ord(key) == 27:
            glutDestroyWindow(1)
            exit(0)

    def loop_func(self, value):
        if random.random() < 0.08:
            self.all_drawable_objects.append(Coin())
        for obj in self.all_drawable_objects:
            obj.tick()
        self.all_drawable_objects = [obj for obj in self.all_drawable_objects if obj.y_offset < 50]
        self.ticks += TICK_INCR
        glutPostRedisplay()
        glutTimerFunc(30, self.loop_func, 0)

    def init(self):
        # initialize the glut library
        glutInit()

        # Init with Double buffering and a depth buffer (to determine what gets
        # rendered on top of what)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH)

        # create a window of size WIDTH by HEIGHT with specified window name
        glutInitWindowSize(WIDTH, HEIGHT)
        glutCreateWindow("This is the window name")

        # set the default background color for when we clear the screen
        glClearColor(.1, .1, .1, 1.0)

        # render items with Z-axis considered.  Otherwise items will just be
        # rendered as they are drawn
        glEnable(GL_DEPTH_TEST)

        # enable lighting.  Otherwise nothing but black and white
        glEnable(GL_LIGHTING)

        # add ambient lighting to the scene
        # more lights could be added with GL_LIGHT1, etc...
        glEnable(GL_LIGHT0)
        lightZeroColor = [0.0, 2.0, 0.8, 1.0]
        glLightfv(GL_LIGHT0, GL_AMBIENT, lightZeroColor)

        # maps points defined in a cube-like x,y,z area to a warped perspective
        # view
        glMatrixMode(GL_PROJECTION)
        # set the perspective of the camera and the min and max Z values to
        # display
        gluPerspective(60.0, WIDTH / HEIGHT, 1., 800.)
        glMatrixMode(GL_MODELVIEW)

        # all subsequent calls will now be applied to the MODELVIEW matrix
        # stack

        # OpenGL event callbacks; call the specified method given the OpenGL
        # callback
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.key_pressed)

        # in 0 milliseconds, call self.loop_func with arbitrary value 0 (unused
        # here)
        glutTimerFunc(0, self.loop_func, 0)

        # Starts event loop, never returns, and calls all the callbacks
        glutMainLoop()

    def display(self):
        # clears the window for both color and depth; color is
        # self-explanatory, and the depth_buffer clearing will prevent items
        # about to be drawn from being rendered behind a now invisible item
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # save the current state of the stack.  Future items pushed onto the
        # matrix can now be transformed independently of the current state
        glPushMatrix()
        self.update_eye()

        for obj in self.all_drawable_objects:
            obj.draw()

        # return to the previous state of the matrix
        glPopMatrix()
        glutSwapBuffers()

        return

if __name__ == '__main__':
    open_gl_example = OpenGLExample()
    open_gl_example.init()
