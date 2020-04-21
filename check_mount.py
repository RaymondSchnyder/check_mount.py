#!/usr/bin/env python
# check_mount.py
# checks if a specific file exists in a docker container

import sys,re,docker
client = docker.from_env()
path_pattern = re.compile('^(\/.+\/)([^\s]+)$')
container_pattern = re.compile('^(\w+)$')

if len(sys.argv) != 3:
    print('you need to provide the container name and the location of the check file like that: ./check_mount.py anaconda /data/check_file')
    exit(1)
# check if container name matches common sense regex (if word)
if not container_pattern.match(sys.argv[1]):
    print("container has an incorrect format")
    exit(1)
# if path matches regex
if not path_pattern.match(sys.argv[2]):
    print("path has an incorrect format!")
    exit(1)
try:
    container=client.containers.get(sys.argv[1])
    # check if checkfile is existing
    if not container.exec_run("test -f {}".format(sys.argv[2]))[0]:
        print("checkfile in container found, everything is fine")
        exit(0)
    else:
        print("checkfile has NOT been found, restart the container")
        exit(1)
except Exception as e:
    print("Docker Exception: {}".format(e))
    exit(1)
