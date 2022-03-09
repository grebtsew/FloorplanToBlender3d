from config.config_handler import ConfigHandler

from random import randint

import string
import random
import os
import hashlib
import sys

"""
FloorplanToBlender3d
Copyright (C) 2022 Daniel Westberg
"""

# TODO make threadsafe!


class shared_variables:
    client_list = []
    all_files = []
    all_ids = []
    all_processes = []
    supported_config_formats = ".ini"
    supported_stacking_formats = ".txt"
    supported_image_formats = (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")
    supported_blender_formats = (
        ".obj",
        ".x3d",
        ".gltf",
        ".mtl",
        ".webm",
        ".blend",
        ".vrml",
        ".usd",
        ".udim",
        ".stl",
        ".svg",
        ".dxf",
        ".fbx",
        ".3ds",
    )

    def __init__(self):
        self.init_config()
        self.init_server_file_structure()
        self.reindex_files()
        self.init_ids()

    def get_object_path(self, id, format=".blend"):
        for file in self.objects:
            if str(id + format) == file:
                return self.parentPath + "/" + self.objectsPath + "/" + id + format
        return None

    def get_process(self, pid):
        for process in self.all_processes:
            if str(process["pid"]) == pid:
                return process
        return None

    def get_file_path(self, id, type_path, list):
        """return full path to file with id, return None if can't be found"""
        for file in list:
            if id in file:
                return self.parentPath + "/" + type_path + "/" + file
        return None

    def reindex_files(self):
        (
            self.all_files,
            self.images,
            self.objects,
            self.stackingfiles,
            self.configfiles,
        ) = self.list_files(self.parentPath)

    def init_ids(self):
        # initialize ids
        for file in self.all_files:
            file_dot_array = file.split(".")
            suffix = file_dot_array[len(file_dot_array) - 1]
            file_no_suffix = file.replace(suffix, "")
            # This will let us know that file already exists!
            tmp = (file_no_suffix, self.hash_generator(file_no_suffix), True)
            if tmp not in self.all_ids:
                self.all_ids.append(tmp)

    def get_id_files(self, id):
        return [
            os.path.join(dp, f)
            for dp, dn, filenames in os.walk("./storage")
            for f in filenames
            if f.replace(os.path.splitext(f)[1], "") == id
        ]

    def bad_client_event(self, client):
        """The purpose of this method is to protect server from harmful requests,
        Using a threshhold, this function increase a bad request counter per client
        """
        # TODO : this!
        # TODO: also add check on all incoming!
        pass

    def get_id(self, id):
        for _id in self.all_ids:
            if id == _id[0]:
                return _id
        return None

    def random_with_N_digits(self, n):
        range_start = 10 ** (n - 1)
        range_end = (10**n) - 1
        return randint(range_start, range_end)

    def pid_exist(self, pid):
        """Go through all processes:s and see if exist"""
        for process in self.all_processes:
            if pid == process["pid"]:
                return True
        return False

    def id_exist(self, id):
        """Go through all id:s and see if exist"""
        for _id, _, _ in self.all_ids:
            if id == _id:
                return True
        return False

    def hash_generator(self, phrase):
        return hashlib.sha224(bytes(phrase, encoding="utf-8")).hexdigest()

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return "".join(random.choice(chars) for _ in range(size))

    def pid_generator(self, size=6):
        return self.random_with_N_digits(size)

    def list_files(self, startpath):
        res = dict()
        all_files = []
        images = []
        configfiles = []
        stackingfiles = []
        objects = []

        for _, _, files in os.walk(startpath):

            for f in files:
                if f.lower().endswith(self.supported_config_formats):
                    configfiles.append(f)
                if f.lower().endswith(self.supported_stacking_formats):
                    stackingfiles.append(f)
                if f.lower().endswith(self.supported_image_formats):
                    images.append(f)
                if f.lower().endswith(self.supported_blender_formats):
                    objects.append(f)
                all_files.append(f)
        return all_files, images, objects, stackingfiles, configfiles

    def init_server_file_structure(self):
        """Creating folders for server files if they do not already exist"""

        if not os.path.exists(self.parentPath):
            os.makedirs(self.parentPath)

        if not os.path.exists(self.parentPath + "/data"):
            os.makedirs(self.parentPath + "/data")

        if not os.path.exists(self.parentPath + "/" + self.imagesPath):
            os.makedirs(self.parentPath + "/" + self.imagesPath)

        if not os.path.exists(self.parentPath + "/" + self.objectsPath):
            os.makedirs(self.parentPath + "/" + self.objectsPath)

        if not os.path.exists(self.parentPath + "/" + self.stackingPath):
            os.makedirs(self.parentPath + "/" + self.stackingPath)

        if not os.path.exists(self.parentPath + "/" + self.configPath):
            os.makedirs(self.parentPath + "/" + self.configPath)

    def init_config(self):
        """Load configs from config file"""
        conf = ConfigHandler()
        [self.flaskHost, self.flaskPort] = conf.get_all("Website")
        self.flaskurl = "http://" + self.flaskHost + ":{0}".format(self.flaskPort)
        self.restapiHost = conf.get("RestApi", "HOST")
        self.restapiPort = conf.get("RestApi", "PORT")

        self.swaggerHost = conf.get("Swagger", "HOST")
        self.swaggerPort = conf.get("Swagger", "PORT")

        self.parentPath = conf.get("Storage", "PARENT")
        self.imagesPath = conf.get("Storage", "IMAGES")
        self.objectsPath = conf.get("Storage", "OBJECTS")
        self.stackingPath = conf.get("Storage", "STACKING")
        self.configPath = conf.get("Storage", "CONFIG")
