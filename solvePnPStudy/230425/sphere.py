import cv2
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutSolidSphere, glutInit, glutInitDisplayMode, glutCreateWindow, GLUT_DOUBLE, GLUT_RGB, GLUT_DEPTH

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutCreateWindow("OpenGL")

cv2.namedWindow("OpenGL")
cv2.imshow("OpenGL", np.zeros((600, 600, 3), dtype=np.uint8))
cv2.waitKey(1)

while True:
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glutSolidSphere(1.0, 20, 20)

    cv2.imshow("OpenGL", np.zeros((600, 600, 3), dtype=np.uint8))
    cv2.waitKey(1)
