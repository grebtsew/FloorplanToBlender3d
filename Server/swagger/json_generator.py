"""
Waits for RestAPI to start
Then collects help functions
And generates a new swagger.json file!
"""
import requests
import time
import json as jsonlib

def wait_for_server(url="http://localhost:8000", validconnectcounter = 10, retrydelay = 5):
    """This function will stall the startup process of swagger gui so we start after rest api is up!
    After X connection retries we will return False, in order to sync status with other GUI!"""
    connected = False
    
    counter = 0
    while not connected:
        try:
            json = {'func': 'help'}
            print("SWAGGER Pending, trying to connect to REST API...")
            requests.get(url, params=json)
            connected = True
            print("SWAGGER Successfully connected to REST API")
        except Exception:
            time.sleep(retrydelay)
            counter+=1
            if counter > validconnectcounter:
                print("SWAGGER max retries exceeded, will restart connection procedure.")
                return connected
    return connected

def get_api_info(url):
    json = {'func': 'help'}
    print("----- Sending help request to get ----- ")
    get = requests.get(url, params=json)
    print(get.json())
    print("----- Sending help request to post ----- ")
    post = requests.post(url, data=jsonlib.dumps(json))
    print(post.json())
    print("----- Sending help request to put ----- ")
    headers = {'Content-Type': 'html/text'}
    put = requests.put(url, headers=headers, data=b'empty', params=json)
    print(put.json())

    json = {'func': 'info'} # query
    print("----- Get info... ----- ")
    info = requests.get(url, params=json)
    print("Printing Rest Api information:")
    print(info.text)

    return info.text, get.json(), post.json(), put.json()

# TODO: implement functions below!
def collect_template():
    f = open('./swagger-json/swagger-template.json', "rb") 
    data = jsonlib.load(f) 
    f.close()

    return data

def generate_json(template,info, get, post, put):
    json = template
    # Create info dict and add it to our json object
    json["tags"] = [{"name":"FloorplanToBlender","description":"RMI functions for handling Floorplan To Blender Rest Api Server.","externalDocs":{"description":"Find out more","url":"https://github.com/grebtsew/FloorplanToBlender3d"}}],
    
    # Create scheme dict and add it to json

    # Create json definitions with appropriate links

    return json

def save_to_file(json_template):
    # Here we write to the .json file
    with open('./swagger-json/swagger.json', 'w') as f:
        jsonlib.dump(json_template, f)

def generate_swagger_json():
    
    # TODO collect rest api url from config!
    url="http://localhost:8000"
    # Wait for api is up
    connection_status = False
    while not connection_status:
        connection_status = wait_for_server(url)
        #TODO set shared_variables status value

    # send get help for post, put and get!
    info, get, post, put = get_api_info(url)

    # Get Templates, read from file!
    json_template = collect_template()
    # Create output for received objects!
    json_new = generate_json(json_template, info, get, post, put)
    # Create final file
    save_to_file(json_new)
    # return success or fail
    return True

generate_swagger_json()
