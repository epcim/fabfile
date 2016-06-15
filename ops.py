"""
Fabfile

Intended to provide scripted interface for common ops actions.

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



## EXECUTION
# def run(c):
    # """ Run given cmd on remote host.
    # Example: fab run:'killall java', exclude_hosts='web' -P
    # """
    # #if _online(env.host) is True:
    # run(c)


## NETWORKING
@task
def routes2gw(cidr='10.8.0.0/16', gw=None):
    env.key_filename = []
    if gw: env.gateway = gw
    sudo("ip ro add %s via %s" % (cidr, env.gateway))


## PROCESSES
@task
def check_proc(process, dry=True):
    """ Check for running process on host
    """
    _credentials(user='root')
    #if _online(env.host) is True:

    with settings(hide('running'), warn_only=dry, skip_bad_hosts=dry):
        #TODO: Return count (pids) - but count them
        o = run('pgrep "%s"| wc -l' % process)
    if o >= 1 and dry != True:
        abort("Aborted: %s java processes is running on host %s" % (o, env.host))


## ACCESS
@task
def bootstrap_keys(password=None):
    if env.key_filename:
        for key in env.key_filename:
            if os.path.isfile(os.path.expanduser(key)):
                push_key(key_file=key+'.pub', user='root', password=password, force=True)



@task
def push_key(key_file='~/.ssh/id_dsa.pub', user=None, password=None, force=False, skipOffline=None):
    """ Append passed ssh pubkey to destination host (if not exist already)
    """
    _skipExcluded()

    if (skipOffline and not _online(env.host)):
        return

    _credentials(user,password)

    print('Uploading key: ',key_file)
    key_text = _read_key_file(key_file).strip()
    run('test -d ~/.ssh || mkdir -p ~/.ssh/')
    append('~/.ssh/authorized_keys', key_text)
    run('chmod 755 ~/.ssh')
    run('chmod 600 ~/.ssh/*')
    run('which restorecon && restorecon -R -v $HOME/.ssh/* || echo NORESTORECONF')



## ########################################################################
## PRIVATE METHODS

def _skipExcluded():
    # Skip excluded hosts
    if env.host in env.exclude_hosts:
        print(red("Excluded"))
        return


def _read_key_file(key_file):
    key_file = os.path.expanduser(key_file)
    if not key_file.endswith('pub'):
        raise RuntimeWarning('Trying to push non-public part of key pair')
    with open(key_file) as f:
        return f.read()


def _online(machine):
    """ Is machine reachable on the network? (ping)
    """
    # Skip excluded hosts
    if env.host in env.exclude_hosts:
        print(red("Excluded"))
        return False

    with settings(hide('everything'), warn_only=True, skip_bad_hosts=True):
        if local("ping -c 2 -W 1 %s" % machine).failed:
            print(yellow('%s is Offline \n' % machine))
            return False
        return True


def _upload_dir(local_dir, remote_dir):
    """Copy a local directory to a remote one, using tar and put. Silently
    overwrites remote directory if it exists, creates it if it does not
    exist."""
    local_tgz = "/tmp/fabtemp.tgz"
    remote_tgz = os.path.basename(local_dir) + ".tgz"
    local('tar -C "{0}" -czf "{1}" .'.format(local_dir, local_tgz))
    put(local_tgz, remote_tgz)
    local('rm -f "{0}"'.format(local_tgz))
    run('rm -Rf "{0}"; mkdir "{0}"; tar -C "{0}" -xzf "{1}" && rm -f "{1}"'\
        .format(remote_dir, remote_tgz))


def _waitForLine(fname, pattern, grepArgs=''):
    """ Wait for string pattern in files
    """
    run("tail -F '%s' | grep -m 1 %s '%s'" % (fname, grepArgs, pattern))


def _fmt(s, **kwargs):
    """
    Recursively interpolate values into the given format string, using
    ``string.Template``.

    The values are drawn from the keyword arguments and ``env``, in that order.
    The recursion means that if a value to be interpolated is itself a format
    string, then it will be processed as well.

    If a name cannot be found in the keyword arguments or ``env``, then that
    format-part will be left untouched.

    Examples::

        >>> fmt("$shell 'echo $PWD'")
        "/bin/bash -l -c 'echo $PWD'"

        >>> fmt("echo $$shell")
        'echo $shell'

        >>> fmt("a is ($a)", a="b is ($b/$c)", b=1, c=2)
        'a is (b is (1/2))'
    """
    data = {}
    data.update(env)
    data.update(kwargs)
    for k, v in data.items():
        if isinstance(v, basestring) and '$' in v:
            data[k] = fmt(v, **data)
    return Template(s).safe_substitute(data)


def _manual(cmd):
    """ Interactive shell execution
    """
    pre_cmd = "ssh -p %(port)s %(user)s@%(host)s export " \
              "TERM=linux && " % env
    local(pre_cmd + cmd, capture=False)


def _background(cmd, sockname="dtach"):
    """ Run tasks in background
        Make sure dtach is installed.
    """
    return run('dtach -n `mktemp -u /tmp/%s.XXXX` %s' % (sockname, cmd))


def _credentials(user=None,password=None,key=None):
    if password:
        env.password = password
    if user:
        env.user = user
    if key:
        env.key_filename = key

    #print 'user:' + env.user
    #print 'pass:' + env.password

#vi: ts=2,sts=2:
