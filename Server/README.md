## Floorplan To Blender Server with Swagger API
The server implementation comes with an automatically generated [Swagger API](https://swagger.io/) page.

![swagger](../Images/swaggerdemo.gif)
This folder contains code for the image to model server.

# About
The purpose of this server is to receive images and transform them into 3d models that can be returned.
The server has been tested in python3 and unity3d C#. 
The server can handle an arbitrary amount of simultaneous clients sending different commands and images.
Checkout the Swagger API generated, to see how to use the API correctly.
All API functions are tested in the ./test/ folder with python3 scripts!

# Getting started

To pull and run the container together in a one line command run:
```bash
# Run this from the root folder!
 docker-compose -f docker-compose.server.yml up
```
**NOTE**: this docker-compose file also starts a weavescope container for monitoring purposes!