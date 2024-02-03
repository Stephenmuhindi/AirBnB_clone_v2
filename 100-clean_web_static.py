#!/usr/bin/python3
"""Deletes out-of-date archives"""
import os
from fabric.api import env, lcd, cd, local, run

env.hosts = ['100.25.102.191', '100.26.162.26']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_clean(number=0):
    """Delete out-of-date archives both localy and
    remotely"""
    number = 1 if int(number) == 0 else int(number)
    releases_directory = "/data/web_static/releases"

    version_archives = sorted(os.listdir('versions'))
    [version_archives.pop() for _ in range(number)]
    with lcd('versions'):
        [local("rm ./{}".format(archive)) for archive in version_archives]

    with cd(releases_directory):
        release_archives = run("ls -tr").split()
        release_archives = [a for a in release_archives if "web_static_" in a]
        [release_archives.pop() for _ in range(number)]
        [run("rm -rf ./{}".format(archive)) for archive in release_archives]
