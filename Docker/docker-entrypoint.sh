#!/bin/bash

echo "--- Starting Script ---"
echo "Incoming parameters "
echo $1

if ["$1" -eq "true"]; then
    echo "Starting server and jupyter"
    jupyter notebook /home/floorplan_to_blender/ --port=8888 --ip=0.0.0.0 --allow-root --no-browser --NotebookApp.token='' &
    cd /home/floorplan_to_blender/Server
    python3 ./main.py
else
    echo "Starting ftb script"
    python3 /home/floorplan_to_blender/create_blender_project_from_floorplan.py
fi

echo "--- Done ---"