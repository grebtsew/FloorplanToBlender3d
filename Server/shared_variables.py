from config.file_handler import ConfigHandler

import os

class shared_variables():
    client_list = []
    all_files = []

    def __init__(self):
        self.init_config()
        self.init_server_file_structure()
        self.reindex_files()

    def reindex_files(self):
        # TODO: make this better!
        self.all_files  = self.list_files(self.parentPath)

        
    def list_files(self, startpath):
        res = dict()
        all_files = []
        
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            #indent = ' ' * 4 * (level)
            #print('{}{}/'.format(indent, os.path.basename(root)))
            #subindent = ' ' * 4 * (level + 1)
            for f in files:
                #print('{}{}'.format(subindent, f))
                all_files.append[f]
        return all_files

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
