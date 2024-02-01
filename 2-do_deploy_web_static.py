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
    """Distributes an archive (already created) to
    your web servers,"""

    if exists(archive_path):
        new_archive_path = archive_path.split("/")[1]duro
        newest_version = "/data/web_static/releases/" + new_archive_path[:-4]

        put(new_archive_path, "/tmp/")
        sudo("mkdir -p {}".format(newest_version))
        sudo("tar -xzf {} -C {}/".format(new_archive_path,
                                             newest_version))
        sudo("rm {}".format(archive_path))
        sudo("mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        sudo("rm -rf {}/web_static".format(newest_version))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True

    return False
