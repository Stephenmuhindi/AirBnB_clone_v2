#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
import time
from fabric.api import *
from os.path import exists

env.hosts = ["100.25.102.191", "100.26.161.26"]
env.user = "ubuntu"


def do_pack():
    """Adds all files in the folder web_static to the final archive"""
    timestamp = time.strftime("%Y%m%d%H%M%S")

    if not exists("versions"):
        local("mkdir -p versions")

    archived_path = "versions/web_static_{}.tgz".format(timestamp)
    start_path = local("tar -cvzf {} web_static".format(archived_path))

    if start_path.succeeded:
        return archived_path
    else:
        None


def do_deploy(archive_path):
    """Deploy web files to server"""
    try:
        if not exists(archive_path):
            return False

        # Upload archive
        put(archive_path, '/tmp/')

        timestamp = archive_path[-1].split('.')[0]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'
            .format(timestamp))

        # Uncompress archive, delete archive, Move files into Host
        # web_static then remove the src web_static dir
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
            /data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
            /data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'
            .format(timestamp))

        # Delete pre-existing sym link and re-establish
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/web_static_{}/ \
            /data/web_static/current'.format(timestamp))
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    # Returns True if successful
    return True


def deploy():
    """Script that creates and distributes an
    archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
