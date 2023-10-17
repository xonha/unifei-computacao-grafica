import random
import sys
from time import sleep

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

from utils import BASE_COLOR, COLORS_LIST, SCENE_COORDINATES, TEXT_COLOR


class Polygons:
    def __init__(
        self,
        x: int,
        y: int,
        z: int,
        id: int,
        index: int,
    ):
        self.position = (x, y, z)
        self.id = id
        self.form_id = int(str(id)[0])
        self.color_id = int(str(id)[1])
        self.index = index
        self.parent_index = (index - 1) // 2
        self.children_indexes = []
        if index < 15:
            self.children_indexes = [index * 2 + 1, index * 2 + 2]
        gl.glShadeModel(gl.GL_FLAT)

    def display(self, active: bool = False):
        if active is False:
            gl.glColor3f(*COLORS_LIST[self.color_id])
        else:
            gl.glColor3f(*TEXT_COLOR)
            gl.glFlush()

        gl.glPushMatrix()
        gl.glTranslatef(*self.position)

        match self.form_id:
            case 1:
                glut.glutSolidCube(1.0)
            case 2:
                glut.glutSolidSphere(0.7, 20, 20)
            case 3:
                glut.glutSolidTeapot(0.6)
            case 4:
                glut.glutSolidTetrahedron()

        gl.glPopMatrix()


class Scene:
    def __init__(self):
        self.rotate_y = 0.0
        self.rotate_x = 0.0
        self.translation_x = 0.0
        self.translation_y = 0.0
        self.scale = 0.2
        self.combinations = random.sample(range(10, 50), 31)
        self.polygons = [
            Polygons(
                *SCENE_COORDINATES[index],
                id=self.combinations[index],
                index=index,
            )
            for index in range(31)
        ]

        glut.glutInit(sys.argv)
        glut.glutInitDisplayMode(glut.GLUT_SINGLE | glut.GLUT_RGB)  # type: ignore
        glut.glutInitWindowSize(800, 800)
        glut.glutCreateWindow("Multiple Cubes")

        glut.glutDisplayFunc(self.display)
        glut.glutReshapeFunc(self.reshape)
        glut.glutSpecialFunc(self.special)
        glut.glutKeyboardFunc(self.keyboard)

        glut.glutMainLoop()

    def dfs(
        self, graph: list[Polygons], start_node: Polygons, target: int, visited=None
    ) -> bool:
        start_node.display(True)
        sleep(1)

        if visited is None:
            visited = set()

        visited.add(start_node.index)

        if start_node.id == target:
            print(visited)
            return True

        for neighbor in start_node.children_indexes:
            if neighbor not in visited:
                if self.dfs(graph, graph[neighbor], target, visited):
                    return True

        return False

    def display(self):
        gl.glClearColor(*BASE_COLOR, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glLoadIdentity()
        glu.gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        gl.glRotatef(self.rotate_x, 1.0, 0.0, 0.0)
        gl.glRotatef(self.rotate_y, 0.0, 1.0, 0.0)
        gl.glScalef(self.scale, self.scale, self.scale)
        gl.glTranslatef(self.translation_x, self.translation_y, 0.0)

        for polygon in self.polygons:
            polygon.display()
            if polygon.parent_index < 0:
                continue

            gl.glColor3f(*TEXT_COLOR)
            gl.glBegin(gl.GL_LINES)
            gl.glVertex3f(*SCENE_COORDINATES[polygon.index])
            gl.glVertex3f(*SCENE_COORDINATES[polygon.parent_index])

            gl.glEnd()

        gl.glFlush()

    def reshape(self, w, h):
        gl.glViewport(0, 0, glu.GLsizei(w), glu.GLsizei(h))
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def special(self, key, x, y):
        if key == glut.GLUT_KEY_RIGHT:
            self.rotate_y += 5
        if key == glut.GLUT_KEY_LEFT:
            self.rotate_y -= 5
        if key == glut.GLUT_KEY_UP:
            self.rotate_x += 5
        if key == glut.GLUT_KEY_DOWN:
            self.rotate_x -= 5
        glut.glutPostRedisplay()

    def keyboard(self, key, x, y):
        if key == b"d":
            self.translation_x -= 0.1
        if key == b"a":
            self.translation_x += 0.1
        if key == b"s":
            self.translation_y += 0.1
        if key == b"w":
            self.translation_y -= 0.1

        if key == b"[":
            self.scale -= 0.1
        if key == b"]":
            self.scale += 0.1

        if key == b"f":
            print("First number is the form id and the second is the color id.\n")
            print("Form id:\n1 = Cube, 2 = Sphere, 3 = Teapot, 4 = Tetrahedron")
            print("\nColor id:")
            print("0 = Blue, 1 = Green, 2 = Maroon, 3 = Mauve")
            print("4 = Peach, 5 = Pink, 6 = Red, 7 = Rosewater")
            print("8 = Sky, 9 = Yellow")

            target_value = int(input("\nEnter the value to search: "))
            if self.dfs(self.polygons, self.polygons[0], target_value):
                print(f"Found {target_value} in the graph.")
            else:
                print(f"{target_value} was not found in the graph.")

        glut.glutPostRedisplay()


if __name__ == "__main__":
    Scene()