#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
from datetime import datetime
from fabric.api import *
import os

env.hosts = ["100.25.102.191", "100.26.161.26"]
env.user = "ubuntu"


def do_pack():
    """Generates a .tgz archive from the contents of the web_static"""

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    start_path = "versions/web_static_{}.tgz".format(date)
    archived_path = local("tar -cvzf {} web_static".format(start_path))

    if archived_path.succeeded:
        return start_path
    else:
        return None


def do_deploy(archive_path):
    """Distribute archive to web servers"""
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        new_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(new_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             new_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(new_version,
                                                new_version))
        run("sudo rm -rf {}/web_static".format(new_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_version))

        print("New version deployed!")
        return True

    return False


def deploy():
    """Script that creates and distributes an
    archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
