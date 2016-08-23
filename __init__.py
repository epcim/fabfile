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
        # if 'hostname' in hive:
           # host = hive['hostname']
        if 'user' in hive:
            host = '%s@%s' % (hive['user'], host)
        if 'port' in hive:
            host = '%s:%s' % (host, hive['port'])
        #print 'hive',hive
        #print 'host',host
        return host

    try:
        config_file = file(expanduser(path))
    except IOError:
        pass
    else:
        config = SSHConfig()
        config.parse(config_file)

        # add hosts from ssh config to env.host & sort + unique
        env.hosts.extend([h for h in config.get_hostnames() if len(h) > 1])
        env.hosts = sorted(set(env.hosts))

        keys = [config.lookup(host).get('identityfile', None) for host in env.hosts]
        # flatten
        keys = [item for sublist in keys  if sublist is not None for item in sublist]
        env.key_filename = [expanduser(key) for key in keys if key is not None]
        env.hosts = [hostinfo(host, config) for host in env.hosts]

        for role, rolehosts in env.roledefs.items():
            env.roledefs[role] = [hostinfo(host, config) for host in rolehosts]


def _populateRoledevsFromHosts():
    """ Generate common roledefs from host names
    """
    # Feel free to customize

    for h in env.hosts:
        # pick hostname (strip user/port)
        host=h.split('@')[-1:][0].split(':')[0]
        # remove
        # - domain
        # - trailing numbers from hostname
        short=host.split('.')[0].strip("0123456789")
        if not env.roledefs.has_key(short): env.roledefs[short] = []
        if not h in env.roledefs[short]:
            env.roledefs[short].append(h)


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

    _populateRoledevsFromHosts()

    #print 'DEBUG roledefs', env.roledefs
    #print 'DEBUG hosts', env.hosts



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
