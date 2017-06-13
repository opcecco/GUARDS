#!/bin/bash

###                                                   ###
#    After flashing Erle Robotics "frambuesa" image,    #
#    connecting to the internet, and enabling SSH,      #
#    run this script to finish drone setup.             #
###                                                   ###


##### Please run as root

# Install copter binaries
apt-get update
apt-get install -y apm-copter-pxfmini

# Enable camera modules on boot
echo "bcm2835-v4l2" >> /etc/modules

# Reboot to apply changes
reboot
