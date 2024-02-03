#!/usr/bin/python3
import os
from fabric.api import env, lcd, cd, local, run

env.hosts = ['100.25.102.191', '100.26.162.26']


def do_clean(number=0):
    """Delete out-of-date archives both localy and 
    remotely"""

    number = 1 if int(number) == 0 else int(number)

    with lcd("versions"):
        archives = sorted(os.listdir("."))
        archives_to_remove = archives[:-number]
        [local("rm {}".format(archive)) for archive in archives_to_remove]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr | grep 'web_static_'").split()
        archives_to_remove = archives[:-number]
        [run("rm -rf {}".format(archive)) for archive in archives_to_remove]
