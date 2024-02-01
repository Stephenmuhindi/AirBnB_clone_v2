#!/usr/bin/python3
"""Generates a .tgz archive from the contents of
the web_static folder"""

from datetime import datetime
from fabric.api import *
from os.path import exists

env.hosts = ["100.25.102.191", "100.26.161.26"]
env.user = "ubuntu"


def do_pack():
    """Adds all files in the folder web_static to the final archive"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    if not exists("versions"):
        local("mkdir -p versions")

    start_path = "versions/web_static_{}.tgz".format(timestamp)
    archive_path = local("tar -cvzf {} -C web_static/ .".format(start_path))

    if archive_path.succeeded:
        return start_path
    else:
        None


def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if exists(archive_path):
        archive_filename = archive_path.split("/")[1]
        without_ext = archive_filename.split(".")[0]
        tmp_path = "/tmp/" + archive_filename
        new_version = "/data/web_static/releases/" + without_ext

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_filename, tmp_path)
        sudo("mkdir -p {}".format(new_version))
        sudo("tar -xzf {} -C {}".format(archive_filename, new_version))
        sudo("rm {}".format(tmp_path))
        sudo("mv {}/web_static/* {}".format(new_version,
                                            new_version))
        sudo("rm -rf {}/web_static".format(new_version))
        sudo("rm -rf /data/web_static/current")
        # Create a new symbolic link
        sudo("ln -s {} /data/web_static/current".format(new_version))
        print("New version deployed!")
        return True
    else:
        return False
