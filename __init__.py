"""
Fabfile
- un*x remote management toolbox
- intended to provide scripted interface for common ops actions

"""

VERSION = 1.0
AUTHOR = "epcim@apealive.net"
URL = "http://github.com/epcim/fabric-toolbox"

# TBD
import sys
import os
import os.path
from string import Template
from fabric.api import env

# Used
from fabric.api import task

import fabcfg
import ops

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


env.settings = {}


@task(alias='e')
def environment(name):
    """ Load environment configuration
    """
    env.update(fabcfg.environments[name])
    for l in env.roledefs.values():
        env.hosts.extend(l)



# Main
if os.getenv('ENVIRONMENT'):
  environment(os.getenv('ENVIRONMENT'))
else:
  k = fabcfg.environments.keys()
  k.sort()
  if k:
    environment(k[0])

#vi: ts=2,sts=2:
