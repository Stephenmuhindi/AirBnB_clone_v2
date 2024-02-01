#!/usr/bin/python3
"""Generates a .tgz archive from the contents of
the web_static folder"""

import time
from fabric.api import local, put, env, sudo
from os.path import exists

env.hosts = ["100.25.102.191", "100.26.161.26"]
env.user = "ubuntu"


def do_pack():
    """Adds all files in the folder web_static to the final archive"""
    timestamp = time.strftime("%Y%m%d%H%M%S")
    try:
        if not exists("versions"):
            local("mkdir -p versions")

        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} -C web_static/ .".format(archive_path))
        return archive_path

    except Exception as e:
        pass

def do_deploy(archive_path):
    """Distribute archive."""
    if exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        sudo("mkdir -p {}".format(newest_version))
        sudo("tar -xzf {} -C {}/".format(archived_file,
                                             newest_version))
        sudo("rm {}".format(archived_file))
        sudo("mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        sudo("rm -rf {}/web_static".format(newest_version))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True

    return False
