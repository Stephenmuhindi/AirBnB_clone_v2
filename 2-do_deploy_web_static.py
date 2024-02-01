#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from datetime import datetime
from fabric.api import env, local, put, run
import os

env.hosts = ["52.91.121.146", "3.85.136.181"]
env.user = "ubuntu"


def do_pack():
    """
    Compress web_static content into a tarball
    """
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(date)
    result = local("tar -cvzf {} web_static".format(archive_path))

    return archive_path if result.succeeded else None


def do_deploy(archive_path):
    """
    Distribute archive to web servers
    """
    if os.path.exists(archive_path):
        remote_path = "/data/web_static/releases/"
        release_folder = "{}{}".format
        (remote_path, archive_path.split("/")[-1][:-4])

        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(release_folder))
        run("sudo tar -xzf /tmp/{} -C {}/".format
            (archive_path.split("/")[-1], release_folder))
        run("sudo rm /tmp/{}".format
            (archive_path.split("/")[-1]))
        run("sudo mv {}/web_static/* {}/".format
            (release_folder, release_folder))
        run("sudo rm -rf {}/web_static".format(release_folder))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(release_folder))

        print("New version deployed!")
        return True

    return False
