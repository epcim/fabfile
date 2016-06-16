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
from fabric.api import env, task, execute, run, runs_once

# Used
from fabric.api import task

# configs
import fabcfg

# aka plugins
import ops
import salt

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


#env.settings = {}

def _annotate_hosts_with_ssh_config_info(path):
    from os.path import expanduser
    from paramiko.config import SSHConfig

    def hostinfo(host, config):
        hive = config.lookup(host)
        #if 'hostname' in hive:
        #    host = hive['hostname']
        if 'user' in hive:
            host = '%s@%s' % (hive['user'], host)
        if 'port' in hive:
            host = '%s:%s' % (host, hive['port'])
        return host

    try:
        config_file = file(expanduser(path))
    except IOError:
        pass
    else:
        config = SSHConfig()
        config.parse(config_file)
        keys = [config.lookup(host).get('identityfile', None)
            for host in env.hosts]
        env.key_filename = [expanduser(key) for key in keys if key is not None]
        env.hosts = [hostinfo(host, config) for host in env.hosts]

        for role, rolehosts in env.roledefs.items():
            env.roledefs[role] = [hostinfo(host, config) for host in rolehosts]


@runs_once
@task(alias='e')
def setenv(name):
    """ Load environment configuration
    """

    cli = env.copy()
    env.update(fabcfg.environments[name])

    #print cli

    # IF ... SPECIFIED ON CLI THEN OVERRIDE
    # gateway
    if cli.has_key('gateway') and cli['gateway'] != None:
        env.gateway = cli['gateway']
    # hosts
    if len(cli['hosts']) > 0:
        env.hosts = cli['hosts']
        #TODO, allow glob* pattern on host name
    else:
      for l in env.roledefs.values():
        env.hosts.extend(l)

    if env.ssh_config_path and os.path.isfile(os.path.expanduser(env.ssh_config_path)):
        env.use_ssh_config = True
        _annotate_hosts_with_ssh_config_info(os.path.expanduser(env.ssh_config_path))



# Main
if os.getenv('FABENV'):
  setenv(os.getenv('FABENV'))
else:
  #print fabcfg.environments
  k = fabcfg.environments.keys()[:]
  k.sort()
  if k:
    setenv(k[0])



#vi: ts=2,sts=2:
