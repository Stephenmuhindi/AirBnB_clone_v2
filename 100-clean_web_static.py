#!/usr/bin/python3
import os
from fabric.api import env, lcd, cd, local, run

env.hosts = ['100.25.102.191', '100.26.162.26']


def do_clean(number=0):
    """Delete out-of-date archives both localy and 
    remotely"""

    number = 1 if int(number) == 0 else int(number)

    with lcd("versions"):
        local_archives = sorted(os.listdir("."))
        [local("rm ./{}".format(arch)) for arch in local_archives[:-number]]

    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr").split()
        remote_archives = [arch for arch in remote_archives if "web_static_" in arch]
        [run("rm -rf ./{}".format(arch)) for arch in remote_archives[:-number]]
