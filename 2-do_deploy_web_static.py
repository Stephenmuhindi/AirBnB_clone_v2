#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers"""
from fabric.api import *
from os.path import exists

env.hosts = ["100.25.102.191", "100.26.161.26"]
env.user = "ubuntu"
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """Deploy web files to server"""
    if not exists(archive_path):
        return False

    # Upload archive
    put(archive_path, '/tmp/')

    timestamp = archive_path.split('.')[0][-14:]
    sudo('mkdir -p /data/web_static/releases/web_static_{}/'.format(timestamp))

    # Uncompress archive, delete archive, Move files into Host
    # web_static then remove the src web_static dir
    sudo('tar -vxzf /tmp/web_static_{}.tgz -C \
         /data/web_static/releases/web_static_{}/'
         .format(timestamp, timestamp))
    sudo('rm /tmp/web_static_{}.tgz'.format(timestamp))
    sudo('mv /data/web_static/releases/web_static_{}/web_static/* \
         /data/web_static/releases/web_static_{}/'
         .format(timestamp, timestamp))
    sudo('rm -rf \
         /data/web_static/releases/web_static_{}/web_static'.format(timestamp))

    # Delete pre-existing sym link and re-establish
    sudo('rm -rf /data/web_static/current')
    sudo('ln -s /data/web_static/releases/web_static_{}/ \
         /data/web_static/current'.format(timestamp))
