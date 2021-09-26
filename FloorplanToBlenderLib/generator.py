import abc
import cv2
import math
import numpy as np

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
        IO.save_to_file(self.path+"wall_vertical_verts", self.verts, info)
        IO.save_to_file(self.path+"wall_vertical_faces", self.faces, info)


        self.verts = []
        for box in boxes:
            self.verts.extend([transform.scale_point_to_vector(box, self.scale, 0)])
            self.verts.extend([transform.scale_point_to_vector(box, self.scale, 1)])

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
        IO.save_to_file(self.path+"wall_horizontal_verts", self.verts, info)
        IO.save_to_file(self.path+"wall_horizontal_faces", self.faces, info)


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

        IO.save_to_file(self.path+"room_verts", self.verts, info)
        IO.save_to_file(self.path+"room_faces", self.faces, info)

        return self.get_shape(self.verts, self.scale)

def get_box_center(box):
    x,y,w,h = cv2.boundingRect(box)
    return (x+w/2, y+h/2)

def euclidean_distance_2d(p1,p2):
    
    return math.sqrt(abs(math.pow(p1[0]-p2[0],2) - math.pow(p1[1]-p2[1],2)))

class Door(Generator):
       
    def get_point_the_furthest_away(self, door_features, door_box):
        best_point = None
        dist = 0
        center = get_box_center(door_box)
        for f in door_features:
            if best_point is None:
                best_point = f
                dist = abs(euclidean_distance_2d(center, f)) 
            else:
                distance = abs(euclidean_distance_2d(center, f))
                if dist < distance :
                    best_point = f
                    dist = distance
        return best_point
    
    def get_closest_point_to_point(self, p , door_features):
        closest_point = None
        dist = math.inf
        for point in door_features:
            if point == p:
                continue
            if closest_point is None:
                closest_point = point
                dist = abs(euclidean_distance_2d(p, point))
            else:
                distance = abs(euclidean_distance_2d(p, point))
                if dist < distance :
                    closest_point = point
                    dist = distance
        return closest_point

    def get_closest_box_point_to_door_point(self, wall_point, box):
        best_points = None
        dists =math.inf

        box_side_points = []
        (x,y,w,h) = cv2.boundingRect(box)

        if w < h :
            box_side_points = [[x+w/2, y],[x+w/2, y+h]]
        else:
            box_side_points = [[x, y+h/2],[x+w, y+h/2]]

        for fp in box_side_points:
            if best_points is None:
                best_points = fp
                dists = euclidean_distance_2d(wall_point, fp)
            else:
                distance = euclidean_distance_2d(wall_point, fp)
                if distance < dists:
                    best_points = fp
                    dists = distance

        return best_points

    def generate(self, gray, info=False):

        doors = detect.doors(gray)

        w = 20
        h = 1

        door_contours = []
        # get best door shapes!
        for door in doors:
            door_features = door[0]
            door_box = door[1]

            # find door to space point
            space_point = self.get_point_the_furthest_away(door_features, door_box)

            # find door to wall corner
            wall_point = self.get_closest_point_to_point(space_point, door_features)

            # find best box corner to use as attachment
            closest_box_point = self.get_closest_box_point_to_door_point(wall_point, door_box)
            
            # Calculate normal
            normal_line = [space_point[0] - closest_box_point[0], space_point[1]-closest_box_point[1]]
            nminval = min(normal_line)
            maxval = max(normal_line)
            for i, val in enumerate(normal_line):
                normal_line[i] = (val/nminval)/(maxval-nminval)

            # Create door contour
            x1 = wall_point[0] + normal_line[0]*w
            y1 = wall_point[1] + normal_line[1]*w

            x2 = space_point[0] - normal_line[0]*w
            y2 = space_point[1] - normal_line[1]*w

            c1 = [x1,y1]
            c2 = [x2,y1]
            c3 = [x2,y2]
            c4 = [x1,y2]
           
            door_contour = np.array([[c1], [c2], [c3], [c4]]) 
            door_contours.append(door_contour)
    

        # TODO: create print script to show debug!

        #Create verts for door
        self.verts, self.faces, door_amount = transform.create_nx4_verts_and_faces(door_contours, self.height, self.scale) # TODO: create 4xn_verts!


        if(info):
            print("Doors created : ", door_amount/4)

        IO.save_to_file(self.path+"door_vertical_verts", self.verts, info)
        IO.save_to_file(self.path+"door_vertical_faces", self.faces, info)
       
        self.verts = []
        for box in door_contours:
            self.verts.extend([transform.scale_point_to_vector(box, self.scale, 0)])
            self.verts.extend([transform.scale_point_to_vector(box, self.scale, 1)])

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
        IO.save_to_file(self.path+"door_horizontal_verts", self.verts, info)
        IO.save_to_file(self.path+"door_horizontal_faces", self.faces, info)

        return self.get_shape(self.verts, self.scale)

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

        IO.save_to_file(self.path+"window_vertical_verts", self.verts, info)
        IO.save_to_file(self.path+"window_vertical_faces", self.faces, info)

        # Fill window form!
        self.verts = []
        for box in windows:
            self.verts.extend([transform.scale_point_to_vector(box, self.scale, 0)])
            self.verts.extend([transform.scale_point_to_vector(box, self.scale, 1)])
            self.verts.extend([transform.scale_point_to_vector(box, self.scale, 0.25)])
            self.verts.extend([transform.scale_point_to_vector(box, self.scale, 0.75)])

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
        IO.save_to_file(self.path+"window_horizontal_verts", self.verts, info)
        IO.save_to_file(self.path+"window_horizontal_faces", self.faces, info)


        return self.get_shape(self.verts, self.scale)
