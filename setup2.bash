#!/bin/bash

###                                                   ###
#    After flashing Erle Robotics "frambuesa" image,    #
#    connecting to the internet, and enabling SSH,      #
#    run this script to finish drone setup.             #
###                                                   ###


# Change amp.sh so that wifi=10.0.0.1:6000



##### Please run as root

# may want to stop apm for speed: systemctl stop apm.service

apt-get update
apt-get install -y python-dev python-opencv python-wxgtk3.0 python-pip python-matplotlib python-pygame python-lxml

pip uninstall -y MAVProxy
pip install future pymavlink

# install mavproxy from source: git clone --depth 1 https://github.com/ArduPilot/MAVProxy.git
# copy the custom modules
# rebuild mavproxy: python setup.py build install --user
# echo 'export PATH=$PATH:$HOME/.local/bin'  >> ~/.bashrc

# Reboot to apply changes
reboot
