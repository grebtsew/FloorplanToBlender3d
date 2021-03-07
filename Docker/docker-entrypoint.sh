#!/bin/bash

echo "--- Starting Script ---"
echo "Incoming parameters "
echo $1

if  [ "$1" = true ]; then
    echo "Moving To server folder"
    cd /home/floorplan_to_blender/Server
    echo "Starting server"
    python3 ./main.py
    
else
    echo "Starting ftb script"
    python3 /home/floorplan_to_blender/create_blender_project_from_floorplan.py
fi

echo "--- Done ---"
