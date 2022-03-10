#!/bin/bash

echo "--- Starting Script ---"
echo "Incoming parameters "
echo $1

if  [ "$1" = "server" ]; then
    echo "Moving To server folder"
    cd /home/floorplan_to_blender/Server
    echo "Starting server"
    python3 ./main.py
elif [ "$1" = "jupyter" ]; then
    echo "Start jupyter notebook on port 8888"
    jupyter notebook /home/floorplan_to_blender/ --port=8888 --ip=0.0.0.0 --allow-root --no-browser --NotebookApp.token=''
else
    echo "Starting ftb script"
    python3.8 /home/floorplan_to_blender/main.py
fi

echo "--- Done ---"
