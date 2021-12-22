"""
Waits for RestAPI to start
Then collects help functions
And generates a new swagger.json file!
"""
"""
FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""
import requests
import time
import json as jsonlib


def wait_for_server(url="http://0.0.0.0:8000", validconnectcounter=10, retrydelay=5):
    """This function will stall the startup process of swagger gui so we start after rest api is up!
    After X connection retries we will return False, in order to sync status with other GUI!"""
    connected = False

    counter = 0
    while not connected:
        try:
            json = {"func": "help"}
            print("SWAGGER Pending, trying to connect to REST API...")
            requests.get(url, params=json)
            connected = True
            print("SWAGGER Successfully connected to REST API")
        except Exception:
            time.sleep(retrydelay)
            counter += 1
            if counter > validconnectcounter:
                print(
                    "SWAGGER max retries exceeded, will restart connection procedure."
                )
                return connected
    return connected


def get_api_info(url):
    json = {"func": "help"}
    print("----- Sending help request to get ----- ")
    get = requests.get(url, params=json)
    # print(get.json())
    print("----- Sending help request to post ----- ")
    post = requests.post(url, data=jsonlib.dumps(json))
    # print(post.json())
    print("----- Sending help request to put ----- ")
    headers = {"Content-Type": "html/text"}
    put = requests.put(url, headers=headers, data=b"empty", params=json)
    # print(put.json())

    json = {"func": "info"}  # query
    print("----- Get info... ----- ")
    info = requests.get(url, params=json)
    # print("Printing Rest Api information:")
    # print(info.text)
    return info.json(), get.json(), post.json(), put.json()


def collect_template():
    f = open("./swagger/swagger-json/swagger-template.json", "rb")
    data = jsonlib.load(f)
    f.close()
    return data


def merge_path_dict(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1:
            dict1[key].update(dict2[key])
        else:
            dict1[key] = value
    return dict1


def get_type_format(class_name):

    if class_name == "<class 'str'>":
        return "string", None
    if class_name == "<class 'int>":
        return "integer", "int64"
    return None, None


def rest_api_to_swagger(type_list):
    res_paths = dict()
    res_defs = dict()
    for method in type_list:
        path = "/?func=" + method["method"]
        for query in method["query"]:
            path += "?" + query + "=" + "{" + query + "}"

        parameter_list = []
        definition_dict = dict()
        return_type = ""
        for key, value in method["annotations"].items():
            if key == "return":
                return_type = value
                continue
            type, format = get_type_format(value)

            tmp = dict()
            if type is not None:
                tmp = {
                    "type": type,
                }
            if format is not None:
                tmp = {"type": type, "format": format}
            definition_dict[key] = tmp
            parameter_list.append(
                {
                    "name": key,
                    "in": key,
                    "description": "Returns " + return_type,
                    "required": True,
                    "type": type,
                    "format": format,
                }
            )

        # TODO: add consume, produce
        # TODO: make all functions work in swagger
        # TODO: update comments in code!
        # TODO: add to default startup

        tmp_dict = dict()
        if len(parameter_list) > 0:
            tmp_dict[method["type"].lower()] = {
                "tags": ["FloorplanToBlender"],
                "summary": method["docs"],
                "description": "Number of required parameters in are "
                + str(method["argc"])
                + "\n"
                + "The following are Query parameters: "
                + str(method["query"])
                + "\n"
                + "The following are Data/Json parameters: "
                + str(list(set(method["argv"]) - set(method["query"]))),
                "operationId": method["type"] + method["method"],
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "parameters": parameter_list,
                "responses": {
                    "200": {
                        "description": "successful operation",
                        "schema": {
                            "$ref": "#/definitions/" + method["type"] + method["method"]
                        },
                    }
                },
                # "security":[]
            }
        else:
            tmp_dict[method["type"].lower()] = {
                "tags": ["FloorplanToBlender"],
                "summary": method["docs"],
                "description": "Number of required parameters in are "
                + str(method["argc"])
                + "\n"
                + "The following are Query parameters: "
                + str(method["query"])
                + "\n"
                + "The following are Data/Json parameters: "
                + str(list(set(method["argv"]) - set(method["query"]))),
                "operationId": method["type"] + method["method"],
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "responses": {
                    "200": {
                        "description": "successful operation",
                        "schema": {
                            "$ref": "#/definitions/" + method["type"] + method["method"]
                        },
                    }
                },
                # "security":[]
            }
        res_paths[path] = tmp_dict

        _type = None
        if method["argc"] <= 0:
            _type, _format = get_type_format(return_type)

        if len(definition_dict) > 0:
            res_defs[method["type"] + method["method"]] = {
                "type": _type,
                "properties": definition_dict,
            }
        else:
            res_defs[method["type"] + method["method"]] = {"type": _type}

    return res_paths, res_defs


def generate_json(template, info, get, post, put):
    json = template
    # Create info dict and add it to our json object

    json["tags"] = [
        {
            "name": "FloorplanToBlender",
            "description": "RMI functions for handling Floorplan To Blender Rest Api Server. \n"
            + "Request Version : "
            + info["request_version"]
            + "\n"
            + "Server Version : "
            + info["server_version"]
            + "\n"
            + "System Version : "
            + info["sys_version"]
            + "\n"
            + "Protocol Version : "
            + info["protocol_version"]
            + "\n"
            + "Supported Image Formats : "
            + str(info["supported_image_formats"])
            + "\n"
            + "Supported Blender Formats : "
            + str(info["supported_blender_formats"])
            + "\n",
            "externalDocs": {
                "description": "Find out more",
                "url": "https://github.com/grebtsew/FloorplanToBlender3d",
            },
        }
    ]

    res_paths = dict()
    res_defs = dict()
    # Create scheme dict and add it to json
    # Create json definitions with appropriate links
    paths, defs = rest_api_to_swagger(get)
    merge_path_dict(res_paths, paths)
    res_defs.update(defs)
    paths, defs = rest_api_to_swagger(post)
    merge_path_dict(res_paths, paths)
    res_defs.update(defs)
    paths, defs = rest_api_to_swagger(put)
    merge_path_dict(res_paths, paths)
    res_defs.update(defs)

    json["paths"] = res_paths
    json["definitions"] = res_defs
    json["host"] = "localhost:8000"

    return json


def save_to_file(json_template):
    # Here we write to the .json file
    with open("./swagger/swagger-json/swagger.json", "w") as f:
        jsonlib.dump(json_template, f)


def generate_swagger_json():

    # TODO collect rest api url from config!
    url = "http://localhost:8000"
    # Wait for api is up
    connection_status = False
    while not connection_status:
        connection_status = wait_for_server(url)
        # TODO set shared_variables status value

    # send get help for post, put and get!
    info, get, post, put = get_api_info(url)

    # Get Templates, read from file!
    json_template = collect_template()
    # Create output for received objects!
    json_new = generate_json(json_template, info, get, post, put)
    # Create final file
    save_to_file(json_new)
    print("Managed to create new swagger.json file!")
    # return success or fail
    return True
