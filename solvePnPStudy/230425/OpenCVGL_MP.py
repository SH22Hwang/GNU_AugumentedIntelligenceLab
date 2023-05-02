import cv2
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)  # 화면 초기화

def draw():
    # 3D 구 그리기
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.0, 1.0, 1.0)
    glutWireSphere(0.1, 20, 20)
    glutSwapBuffers()

def display():
    # 웹캠으로부터 이미지 읽어오기
    ret, frame = cap.read()
    if ret:
        # OpenGL 초기화
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, 1.0, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

        # 3D 구 그리기
        draw()

        # 화면에 이미지 출력
        cv2.imshow('frame', frame)

        # ESC 키 입력 시 종료
        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()

if __name__ == '__main__':
    # OpenCV VideoCapture 객체 생성
    cap = cv2.VideoCapture(0)

    # OpenGL 초기화
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow("OpenGL")

    # 콜백 함수 등록
    glutDisplayFunc(display)
    glutIdleFunc(display)
    init()

    # 이벤트 루프 시작
    glutMainLoop()
