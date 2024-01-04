#!/bin/bash
# This file contains bash commands that will be executed at the beginning of the container build process,
# before any system packages or programming language specific package have been installed.
#
# Note: This file may be removed if you don't need to use it
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends tzdata
ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime
dpkg-reconfigure --frontend noninteractive tzdata
apt-get install -y cmake zip unzip
apt-get clean
rm -rf /var/lib/apt/lists/*

mkdir -p /mnt/docs