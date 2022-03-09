import os
from sys import platform


def find_files(filename, search_path):
    """
    Find filename in root search path
    """
    for root, _, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None


def blender_installed():
    if platform == "linux" or platform == "linux2":
        # linux
        return find_files("blender", "/")
    elif platform == "darwin":
        # OS X
        return find_files("blender", "/")
    elif platform == "win32":
        # Windows
        return find_files("blender.exe", "C:\\")


print(blender_installed())
