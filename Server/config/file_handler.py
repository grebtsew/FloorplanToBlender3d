import configparser

class FileHandler():
    def __init__(self):
        pass

    def init_files(self):
        pass


class ConfigHandler():

    def __init__(self, path="config/config.ini"):
        self.path = path
        self.config = self.readconfig_file()

    def readconfig_file(self):
        config = configparser.ConfigParser()
        config.read(self.path)
        return config

    def __str__(self):
        print("List all contents")
        for section in self.config.sections():
            print("Section: %s" % section)
            for options in self.config.options(section):
                print("x %s:::%s:::%s" % (options,
                                          self.config.get(section, options),
                                          str(type(options))))
    def get_all(self, section):
        res = []
        for options in self.config.options(section):
            res.append(self.config.get(section, options))
        return res

    def get(self, section, value):
        return self.config.get(section, value)
    def getboolean(self, section, value):
        return self.config.getboolean(section,value)