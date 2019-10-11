#!/bin/sh

# for now we depend on the ROS python modules from the global site packages...
virtualenv -p python2.7 --system-site-packages venv
venv/bin/pip install -r requirements.txt pytest
