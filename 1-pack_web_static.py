#!/usr/bin/python3
"""Generates a .tgz archive from the contents of
the web_static folder"""

import time
from fabric.api import local
from os.path import exists


def do_pack():
    """Adds all files in the folder web_static to the final archive"""
    timestamp = time.strftime("%Y%m%d%H%M%S")

    if not exists("versions"):
        local("mkdir -p versions")

    start_path = "versions/web_static_{}.tgz".format(timestamp)
    archive_path = local("tar -cvzf {} web_static".format(start_path))

    if archive_path.succeeded:
        return start_path
    else:
        None
