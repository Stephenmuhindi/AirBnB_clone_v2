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
    archive_path = local("tar -cvzf {} web_static".format(start_path))

    if archive_path.succeeded:
        return start_path
    else:
        None


def do_deploy(archive_path):
    """Distribute archive file to the server(s)"""
    if exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             newest_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        run("sudo rm -rf {}/web_static".format(newest_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True

    return False
