#!/usr/bin/python3
"""Generates a .tgz archive from the contents of
the web_static folder"""

from fabric.api import local, run
from os.path import exists
import time


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
