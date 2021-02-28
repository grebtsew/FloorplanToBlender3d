import cv2
import pywavefront
import os
import requests
import json as jsonlib
import time

"""
This files purpose of this file is to test core functionallity of the server.
We also test some common problems.
"""
path_to_test_image="../Images/example.png"
path_to_result_folder="./test-result"

url="http://127.0.0.1:8000"

if __name__ == "__main__":
    # Create folder to play around with
    if not os.path.exists(path_to_result_folder):
        os.makedirs(path_to_result_folder)
        print("Created test folder.")

    # Load image file
    print("Loading image...")
    image = cv2.imread(path_to_test_image, 0) 

    # Get some information
    json = {'func': 'info'} # query
    print("----- Get info... ----- ")
    response = requests.get(url, params=json)
    print(response)
    print("Printing Rest Api information:")
    print(response.text)
    print("DONE!")

    # GET entire table
    json = {'func': 'all'} # query
    print("----- Get all files... ----- ")
    response = requests.get(url, params=json)
    print(response)
    print("Printing file array:")
    print(response.text)
    print("DONE!")
    
    # GET and show all images on server
    json = {'func': 'images'}
    response = requests.get(url, params=json)
    print("----- Get Images ----- ")
    print(response)
    print(response.text)
    print("DONE!")

    # GET and show all objects on server
    json = {'func': 'objects'}
    print("----- Get Objects ----- ")
    response = requests.get(url, params=json)
    print(response)
    print(response.text)
    print("DONE!")

    # send POST request to get new file ID
    json = {'func': 'create'}
    print("----- POST create new file ----- ")
    response = requests.post(url, data=jsonlib.dumps(json))
    print(response)
    print(response.text)
    print("DONE!")

    # Handle response
    try:
        pair = list(eval(response.text))
    except Exception as e:
        print("ERROR: " + str(e), " \n With response:" ,response.text)
        exit()
    id = pair[0]
    hash= pair[1]

    # send PUT image file to id
    print("----- PUT upload new file ----- ")
    with open(path_to_test_image, 'rb') as infile:
        json = {'func': 'create', 'id':id, 'hash':hash, 'format':'.jpg'}
        headers = {'Content-Type': 'multipart/form-data'}
        response = requests.put(url, data=infile, params=json, headers=headers)
    # TODO test sending to id that already exists
    print(response)
    print(response.text)
    print("DONE!")

    #  Test sending to id that already exists
    print("----- PUT upload same file ----- ")
    with open(path_to_test_image, 'rb') as infile:
        json = {'func': 'create', 'id':id, 'hash':hash, 'format':'.jpg'}
        headers = {'Content-Type': 'multipart/form-data'}
        response = requests.put(url, data=infile, params=json, headers=headers)
    print(response)
    print(response.text)
    print("Test Passed!")
    print("DONE!")

    # send POST command to create .obj from image id
    json = {'func': 'transform', 'id':id, 'format':'.obj'}
    print("----- POST transform image "+id+" into 3d model of format .obj ----- ")
    response = requests.post(url, data=jsonlib.dumps(json))
    print(response)
    print(response.text)
    print("DONE!")

    # send GET all processes
    json = {'func': 'processes'}
    print("----- GET all processes ----- ")
    response = requests.get(url, params=json)
    print(response)
    print(response.text)
    print("DONE!")

    # send GET one process 
    pid = 0
    json = {'func': 'process', 'pid':pid}
    print("----- GET "+str(pid)+" process ----- ")
    response = requests.get(url, params=json)
    print(response)
    print(response.text)
    print("DONE!")

    # send PUT and create object
    with open(path_to_test_image, 'rb') as infile:
        json = {'func': 'createandtransform', 'id':id, 'format':'.jpg', 'output':'.obj'}
        headers = {'Content-Type': 'multipart/form-data'}
        response = requests.put(url, data=infile, params=json, headers=headers)
    print(response)
    print(response.text)
    print("Test Passed!")
    print("DONE!")

    # get download and show image
    json = {'func': 'image', 'id': id}


    # get download and show .obj file
    json = {'func': 'object', 'id': id}
    

    #scene = pywavefront.Wavefront('something.obj')

    # send post to remove file & object!
    json = {'func': 'remove', 'id': id}

    # send get help for post, put and get!
