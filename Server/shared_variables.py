from config.file_handler import ConfigHandler

from random import randint

import string
import random
import os
import hashlib

class shared_variables():
    client_list = []
    all_files = []
    all_ids = []
    all_processes = []
    supported_image_formats = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
    supported_blender_formats = ('.obj','.x3d','.webm','.vrml','.usd','.udim','.stl','.svg','.dxf','.fbx','.3ds')
    
    def __init__(self):
        self.init_config()
        self.init_server_file_structure()
        self.reindex_files()
        self.init_ids()

    def get_image_path(id):
        """return full path to file with id, return None if can't be found"""
        pass

    def reindex_files(self):
        # TODO: make this better by saving dicts
        self.all_files, self.images, self.objects  = self.list_files(self.parentPath)

    def init_ids(self):
        # initialize ids
        for file in self.all_files:
            file_dot_array = file.split(".")
            suffix = file_dot_array[len(file_dot_array)-1]
            file_no_suffix = file.replace(suffix,"")
            # This will let us know that file already exists!
            self.all_ids.append((file_no_suffix, self.hash_generator(file_no_suffix), True))

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
        range_start = 10**(n-1)
        range_end = (10**n)-1
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
        return hashlib.sha224(bytes(phrase, encoding='utf-8')).hexdigest()

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def pid_generator(self, size=6):
        return self.random_with_N_digits(size)

    def list_files(self, startpath):
        res = dict()
        all_files = []
        images = []
        objects = []
        
        for root, dirs, files in os.walk(startpath):
            #level = root.replace(startpath, '').count(os.sep)
            #indent = ' ' * 4 * (level)
            #print('{}{}/'.format(indent, os.path.basename(root)))
            #subindent = ' ' * 4 * (level + 1)
            for f in files:
                #print('{}{}'.format(subindent, f))
                if(f.lower().endswith(self.supported_image_formats)):
                    images.append(f)
                if(f.lower().endswith(self.supported_blender_formats)):
                    object.append(f)
                all_files.append(f)
        return all_files, images, objects

    def init_server_file_structure(self):
        """Creating folders for server files if they do not already exist"""
        
        if not os.path.exists(self.parentPath):
            os.makedirs(self.parentPath)
        
        if not os.path.exists(self.parentPath+"/"+self.imagesPath):
            os.makedirs(self.parentPath+"/"+self.imagesPath)

        if not os.path.exists(self.parentPath+"/"+self.objectsPath):
            os.makedirs(self.parentPath+"/"+self.objectsPath)

    def init_config(self):
        """Load configs from config file"""
        conf = ConfigHandler()
        [self.flaskHost, self.flaskPort] = conf.get_all("Website") 
        self.flaskurl = "http://"+self.flaskHost+":{0}".format(self.flaskPort)
        [self.restapiHost, self.restapiPort] = conf.get_all("RestApi")

        self.parentPath = conf.get("Storage","PARENT")
        self.imagesPath = conf.get("Storage","IMAGES")
        self.objectsPath = conf.get("Storage","OBJECTS")
