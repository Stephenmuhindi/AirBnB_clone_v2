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
    """Deploys the tar archive to the server and unpacks it"""
    dir_name = archive_path.split("/")[1]
    if not exists(archive_path):
        return False

    upload_file = put(archive_path, "/tmp/")
    if upload_file.failed:
        return False

    create_dir = sudo("mkdir -p /data/web_static/releases/{}".
                     format(dir_name[:-4]))
    if create_dir.failed:
        return False

    unpack = sudo("tar -xzf /tmp/{} -C /data/web_static/releases/{}".
                 format(dir_name, dir_name[:-4]))
    if unpack.failed:
        return False

    rm_dir = sudo("rm /tmp/{}".format(dir_name))
    if rm_dir.failed:
        return False

    move_file = sudo("mv /data/web_static/releases/{}/web_static/* \
                    /data/web_static/releases/{}/".
                    format(dir_name[:-4], dir_name[:-4]))
    if move_file.failed:
        return False

    rm_not_needed = sudo("rm -rf /data/web_static/releases/{}/web_static/".
                        format(dir_name[:-4]))
    if rm_not_needed.failed:
        return False

    rm_sym = sudo("rm /data/web_static/current")
    if rm_sym.failed:
        return False

    make_sym = sudo("ln -sf /data/web_static/releases/{} \
                   /data/web_static/current".format(dir_name[:-4]))
    if make_sym.failed:
        return False

    return True
