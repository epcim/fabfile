"""
Fabfile

Intended to provide scripted interface to take actions on ubuntu servers.

"""
AUTHOR = "epcim@apealive.net"
URL = "http://github.com/epcim/fabfile"

from fabric.api import *
@task

# @runs_once
# def help():
  # print """
  # """

@task
def cmd(cmd):
    run("%s" % (cmd))

@task
def add_repo(args,repo=None):
    pass

