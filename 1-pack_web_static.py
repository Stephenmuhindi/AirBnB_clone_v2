#!/usr/bin/python3
"""
dev .tgz archive from web_static
"""
from fabric.api import task, local
from datetime import datetime


@task
def do_pack():
    """
    function ya number 1
    """
    formatted_dt = datetime.now().strftime('%Y%m%d%H%M%S')
    mkdir = "mkdir -p versions"
    path = "versions/web_static_{}.tgz".format(formatted_dt)
    print("Packing web_static to {}".format(path))
    if local("{} && tar -cvzf {} web_static".format(mkdir, path)).succeeded:
        return path
    return None
