import abc
import cv2

from . import detect
from . import transform
from . import IO
from . import const

class Generator():
    __metaclass__ = abc.ABCMeta
    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []
    # Height of waLL
    height = const.WALL_HEIGHT
    # Scale pixel value to 3d pos
    scale = const.PIXEL_TO_3D_SCALE
    # Index is many for when there are several floorplans
    path = ""

    def __init__(self, gray, path, info=False):      
        self.path = path  
        self.shape = self.generate(gray, info)
        

    def get_shape(self, verts, scale):
        '''
        Get shape
        Rescale boxes to specified scale
        @Param verts, input boxes
        @Param scale to use
        @Return rescaled boxes
        '''
        if len(verts) == 0:
            return [0,0,0]

        posList = transform.verts_to_poslist(verts)
        high = [0,0,0]
        low = posList[0]

        for pos in posList:
            if pos[0] > high[0]:
                high[0] = pos[0]
            if pos[1] > high[1]:
                high[1] = pos[1]
            if pos[2] > high[2]:
                high[2] = pos[2]
            if pos[0] < low[0]:
                low[0] = pos[0]
            if pos[1] < low[1]:
                low[1] = pos[1]
            if pos[2] < low[2]:
                low[2] = pos[2]

        return [high[0] - low[0],high[1] - low[1],high[2] - low[2]]

    @abc.abstractmethod
    def generate(self, gray, info=False):
        """Perform the generation"""
        pass

class Floor(Generator):

    def generate(self, gray, info=False):
       
        # detect outer Contours (simple floor or roof solution)
        contour, img = detect.detectOuterContours(gray)
        #Create verts
        self.verts = transform.scale_point_to_vector(contour, self.scale, self.height)

        # create faces
        count = 0
        for _ in self.verts:
            self.faces.extend([(count)])
            count += 1

        if(info):
            print("Approximated apartment size : ", cv2.contourArea(contour))

        IO.save_to_file(self.path+"floor_verts", self.verts, info)
        IO.save_to_file(self.path+"floor_faces", self.faces, info)

        return self.get_shape(self.verts, self.scale)

class Wall(Generator):

    def generate(self, gray, info=False):
        # create wall image (filter out small objects from image)
        wall_img = detect.wall_filter(gray)
        # detect walls
        boxes, img = detect.detectPreciseBoxes(wall_img)

        # Convert boxes to verts and faces
        self.verts, self.faces, wall_amount = transform.create_nx4_verts_and_faces(boxes, self.height, self.scale)

        if(info):
            print("Walls created : ", wall_amount)

        # One solution to get data to blender is to write and read from file.
        IO.save_to_file(self.path+"wall_verts", self.verts, info)
        IO.save_to_file(self.path+"wall_faces", self.faces, info)
        return self.get_shape(self.verts, self.scale)

class TopWall(Generator):
   
    def generate(self, gray, info=False):
         # create wall image (filter out small objects from image)
        wall_img = detect.wall_filter(gray)

        # detect walls
        boxes, img = detect.detectPreciseBoxes(wall_img)

        # Convert boxes to verts and faces
        self.verts, self.faces, wall_amount = transform.create_nx4_verts_and_faces(boxes, self.height, self.scale)

        self.verts = []
        for box in boxes:
            self.verts.extend([transform.scale_point_to_vector(box, self.scale, 0)])

        # create faces
        self.faces = []
        for room in self.verts:
            count = 0
            temp = ()
            for _ in room:
                temp = temp + (count,)
                count += 1
            self.faces.append([(temp)])

        # One solution to get data to blender is to write and read from file.
        IO.save_to_file(self.path+"top_wall_verts", self.verts, info)
        IO.save_to_file(self.path+"top_wall_faces", self.faces, info)

        return self.get_shape(self.verts, self.scale)

class Room(Generator):
    def __init__(self, gray, path, info=False):
        self.height = const.WALL_HEIGHT - 0.001 # place room slightly above floor
        super().__init__( gray, path, info)
       
    def generate(self, gray, info=False):
        gray = detect.wall_filter(gray)
        gray = ~gray
        rooms, colored_rooms = detect.find_rooms(gray.copy())
        gray_rooms =  cv2.cvtColor(colored_rooms,cv2.COLOR_BGR2GRAY)

        # get box positions for rooms
        boxes, gray_rooms = detect.detectPreciseBoxes(gray_rooms, gray_rooms)

        self.verts = []
        #Create verts
        room_count = 0
        for box in boxes:
            self.verts.extend([transform.scale_point_to_vector(box, self.scale, self.height)])
            room_count+= 1

        self.faces = []
        # create faces
        for room in self.verts:
            count = 0
            temp = ()
            for _ in room:
                temp = temp + (count,)
                count += 1
            self.faces.append([(temp)])

        if(info):
            print("Number of rooms detected : ", room_count)

        IO.save_to_file(self.path+"rooms_verts", self.verts, info)
        IO.save_to_file(self.path+"rooms_faces", self.faces, info)

        return self.get_shape(self.verts, self.scale)

class Door(Generator):
       
    def generate(self, gray, info=False):

    
        doors = detect.doors(gray)

        
        
        #Create verts for door
        #verts, faces, door_amount = transform.create_nx4_verts_and_faces(doors, self.height, self.scale)

        #if(info):
        #    print("Doors created : ", door_amount)

        #IO.save_to_file(self.path+"doors_verts", self.verts, info)
        #IO.save_to_file(self.path+"doors_faces", self.faces, info)
        return None
        #return self.get_shape(self.verts, self.scale)

class Window(Generator):
       
    def generate(self, gray, info=False):

        
        windows = detect.windows(gray)
        
        '''
        Windows
        '''
        
        #Create verts for window
        v, self.faces, window_amount1 = transform.create_nx4_verts_and_faces(windows, height=0.25, scale=self.scale) # create low piece
        v2, self.faces, window_amount2 = transform.create_nx4_verts_and_faces(windows, height=1, scale=self.scale, ground= 0.75) # create higher piece

        # TODO: also fill small gaps between windows and walls
        # TODO: also add verts for filling gaps

        self.verts = v
        self.verts.extend(v2)
        parts_per_window = 4
        window_amount = len(v)/parts_per_window

        if(info):
            print("Windows created : ", window_amount)

        IO.save_to_file(self.path+"windows_verts", self.verts, info)
        IO.save_to_file(self.path+"windows_faces", self.faces, info)
        return self.get_shape(self.verts, self.scale)
