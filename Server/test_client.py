from enums import *

"""
This files purpose of this file is to test core functionallity of the server.
"""

# Load image file

# GET entire table
json = {'cmd': CMD_GET.ALL}

# GET and show all images on server
json = {'cmd': CMD_GET.IMAGES}

# GET and show all objects on server
json = {'cmd': CMD_GET.OBJECTS}

# send POST request to get new file ID
json = {'cmd': CMD_POST.CREATE}

# send PUT image file to id
# TODO test sending to wrong id
json = {'cmd': CMD_PUT.SEND, 'id':id, 'hash':hash, 'format':'jpg'}

# send POST command to  to create .obj from image id
json = {'cmd': CMD_POST.TRANSFORM, 'id':id, 'format':'obj'}

# send PUT and create object
json = {'cmd': CMD_PUT.SENDCREATE, 'id':id, 'format':'jpg', 'create':'obj'}

# get status from creation process
json = {'cmd': CMD_GET.PROCESSES}

# get download and show image
json = {'cmd': CMD_GET.IMAGE, 'id': id}

# get download and show .obj file
json = {'cmd': CMD_GET.OBJECT, 'id': id}

import pywavefront
scene = pywavefront.Wavefront('something.obj')

# send post to remove file
json = {'cmd': CMD_POST.REMOVE 'id':id}
