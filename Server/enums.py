from enum import Enum

class CMD_POST(Enum):
    CREATE = 0
    REMOVE = 1
    TRANSFORM = 2

class CMD_GET(Enum):
    ALL = 0
    IMAGES = 1
    OBJECTS = 2
    PROCESSES = 3
    IMAGE = 4
    OBJECT = 5

class CMD_PUT(Enum):
    SEND = 0
    SENDCREATE = 1
