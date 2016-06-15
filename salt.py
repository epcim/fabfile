"""
Fabfile

Intended to provide scripted interface to take actions on salt master.

"""
AUTHOR = "epcim@apealive.net"
URL = "http://github.com/epcim/fabric-toolbox"

import sys
import os
import os.path
import time
from fabric.api import *
from fabric.colors import *
from fabric.contrib.files import append, exists, comment, contains
from fabric.contrib.console import confirm
from string import Template
from fabric.api import env

#import fabcfg as my

## TUTORIAL
##
##  http://wiki.fabfile.org/Recipes
##  http://docs.fabfile.org/en/1.4.3/#api-documentation
##
##     run("cmd", pty=False, combine_stderr=True)
##     local("cmd", capture=True)
##     require('hosts', provided_by=[local,slice])
##
## BUILT-IN COMANDS
##    abort, cd, env, get, hide, hosts, local, prompt,  put, require, roles, run, runs_once,
##    settings, show, sudo, warn
##
## USAGE
##    fab --list
##    fab --list-format=nested --list


#env.hosts = env.roledefs['master'][0]
#env.hosts = ['cfg01']

@task
@roles('master')
def _run(args,hosts='*', cmd='salt'):
    run("%s %s" % (cmd,args))

@task
@roles('master')
def salt(args=None):
    if args:
        _run(args)

# @task
# @roles('master')
# def saltcall(args):
    # salt("salt-call", args)

