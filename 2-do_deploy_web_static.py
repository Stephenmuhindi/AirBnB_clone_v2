#!/usr/bin/python3
"""
rada ya hii namba 2?
"""
from os.path import exists, basename, splitext
from datetime import datetime
from fabric.api import env, task, put, local, sudo, run
env.use_ssh_config = True
env.hosts = ["54.208.23.155", "34.239.255.201"]


def do_pack():
    """
    Fun
    """
    file = "versions/web_static_{}.tgz".format(
            datetime.now().strftime('%Y%m%d%H%M%S')
            )
    print("Packing web_static to {file}".format(file))
    if local("mkdir -p versions && tar -cvzf {file} web_static".format(file)).succeeded:
        return file
    return None


def do_deploy(archive_path):
    """
    fungshon documendation
    """
    try:
        if not exists(archive_path):
            return False
        exte = basename(archive_path)
        no_ext, ext = splitext(exte)
        web_static_dir = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        commands = [
                "rm -rf {}{}/".format(web_static_dir, no_ext),
                "mkdir -p {}{}/".format(web_static_dir, no_ext),
                "tar -xzf /tmp/{} -C {}{}/".format(exte, web_static_dir, no_ext),
                "rm /tmp/{}".format(archive_path),
                "mv {0}{1}/web_static/* {0}{1}/".format(web_static_dir, no_ext),
                "rm -rf {}{}/web_static".format(web_static_dir, no_ext),
                "rm -rf /data/web_static/current",
                "ln -s {}{}/ /data/web_static/current".format(web_static_dir, no_ext),
                ]
        for command in commands:
            sudo(command)
        print("New version deployed!")
        return True
    except Exception:
        return False
