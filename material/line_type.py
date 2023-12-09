from enum import Enum
from OpenGL.GL import *


class LineType(Enum):

    loop = GL_LINE_LOOP
    segments = GL_LINES
    connected = GL_LINE_STRIP
