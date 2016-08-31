"""
Fabfile

Intended to provide scripted interface to take actions on salt master.

"""
AUTHOR = "epcim@apealive.net"
URL = "http://github.com/epcim/fabfile"

#import sys
#import os
#import os.path
#import time

from fabric.api import *
#from fabric.api import env, task, execute, run, runs_once

#from fabric.colors import *
#from fabric.contrib.files import append, exists, comment, contains
#from fabric.contrib.console import confirm
#from string import Template
#from fabric.api import env

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


## TIPS
# fab salt.help


@task
@roles('master')
def ssh_config(grep='',grepv='=127\|=192'):
    if len(grep) > 0:
        grep="|egrep '%s'" % grep
    payload= """
    which jq || apt install -y jq
    declare -A aa;
    eval $(salt \* grains.item ipv4 --out=json --static| jq -r 'to_entries | map({name:.key, ip:.value["ipv4"]})|.[]| "aa["+.name+"]="+.ip[]' |sort|grep -v '%s' %s);
    IFS=$'\n' sorted_keys=($(sort <<<"${!aa[*]}"))
    for i in "${sorted_keys[@]}"; do echo -e "Host ${i}\n  Hostname ${aa[$i]}\n  #User\n  #IdentityFile\n  #Port 22\n\n";done
    """ %(grepv, grep)
    cmd(payload)

#env.hosts = ['cfg01']

@task
@runs_once
def help():
  print """

    # NOTE:
    # there is and <fabfile repo>/.fabrc.openstack.example for inspiration

    export DOMAIN=openstack.local

    function escape() {
        E=$@
        # stupid, but works in multiple shells
        #E=${E//\*/\\\*}
        E=${E//\,/\\\,}
        E=${E//\'/\\\'}
        E=${E//\:/\\\:}
        E=${E//\~/\\\~}
        E=${E//\;/\\\;}
        E=${E//\&/\\\&}
        E=${E//\|/\\\|}
        echo ${E}
    }

    # shell shortcuts
    function fabsalt()    { action=$1;shift;X="$@"; fab salt.$action:"$(escape $X)" };
    function control()    { H=$1;shift;X=$@; fab salt.cmd:"$H","source /root/keystonerc${OS_TENANT:+_$OS_TENANT}; $(escape $X)" }
    function compute()    { X=$@; fab salt.cmd:hosts="cmp01${DOMAIN:+.$DOMAIN}","source /root/keystonerc;${X//\*/\*}" }
    function fabhost()    { H=$1;shift;X=$@; fab salt.cmd:"$H","$(escape $X)" }
    function smaster()    { X=$@; fab salt.cmd:role='master',"${X//\*/\*}" }


    # example openstack topology shortcuts
    alias smasters\#="fabhost roles=cfg"
    alias contrails\#="fabhost roles=ntw"
    alias databases\#="fabhost roles=dbs"
    alias controllers\#="control roles=ctl"
    alias ctl\#="control hosts=ctl01${DOMAIN:+.$DOMAIN}"
    alias kvm\#="fabhost hosts=kvm01${DOMAIN:+.$DOMAIN}"
    alias cfg\#="fabhost hosts=cfg01${DOMAIN:+.$DOMAIN}"
    alias cmp\#="fabhost hosts=cmp01${DOMAIN:+.$DOMAIN}"
    alias dbs\#="fabhost hosts=dbs01${DOMAIN:+.$DOMAIN}"
    alias mtr\#="fabhost hosts=mtr01${DOMAIN:+.$DOMAIN}"
    alias ntw\#="fabhost hosts=ntw01${DOMAIN:+.$DOMAIN}"
    alias anl\#="fabhost hosts=anl01${DOMAIN:+.$DOMAIN}"

    # optionally
    #alias salt="fabsalt salt";
    #alias salt-key="fabsalt key";
    #alias salt-call="fabsalt call";
    #alias salt-cmd="fabsalt cmd";

    ## direct execution
    # salt ctl\* grains.get ipv4
    # salt ctl\* state.highstate
    # fab -H ctl01 salt.call:"state.sls linux"
    # fab salt.call:"state.sls linux",roles=ctl
    # fab -g 10.10.15.3 --skip-bad-hosts setenv:vpc20 salt.cmd:"hostname -I"
    #
    ## using a wrapper
    # cfg# salt-call state.sls linux,openssh
    # cfg# salt kvm\* state.sls linux,openssh,libvirt
  """

@task
def cmd(cmd,sudo_user='root',use_sudo=True):
    with settings(sudo_user=sudo_user,use_sudo=use_sudo):
        sudo("%s" % (cmd))

@task
@roles('master')
def salt(args,cmd='salt'):
    if args:
      # merge attribute after salt module name, module name identified as containing '.'
      remap=[]
      for i,e in enumerate(args.split()+['','']):
        print 'DEBUG', i,e
        if '.' not in e :
            print t[i]
            remap.append(t[i])
        else:
            remap.extend([t[i], " ".join(t[i+1:]).strip()])
            break
      # quote by ''
      args_qouted=" ".join("'%s'" % i for i in remap if i <> '' )
      run("%s %s" % (cmd, args_qouted))
      #execute(_run(args))

@task
@roles('master')
def call(args):
    salt(args, cmd="salt-call")

@task
@roles('master')
def key(args):
    salt(args, "salt-key")

@task
def sync():
  "Sync working directory with salt master"
  pass
  # TODO, upload reclas dir/repo
  # TODO, upload nodes dir/repo + restar saltmaster ????




## TO BE EVALUATED/UPDATED, use with caution
## https://github.com/marselester/salt-stack-example/blob/master/fabfile.py
## http://codegists.com/search/fabfile/

from fabric.api import env, task, run, runs_once, sudo, put, cd, abort
from fabric.contrib.project import upload_project
from fabric.contrib.files import exists

env.salt_env_name = None


@task
@runs_once
def salt_env(name):
    """Which Salt environment to deploy?
    There are following Salt environments:
    - ``dev, development`` -- contains well known credentials and libraries
      which facilitate development.
    - ``prd, production`` -- contains production credentials.
    """
    if name in ('dev', 'prd'):
        env.salt_env_name = name
    else:
        abort('Unknown Salt environment.')


@task
@runs_once
def bootstrap_salt():
    """Bootstraps Salt installation."""
    with cd('/tmp/'):
        run('wget -O - http://bootstrap.saltstack.org | sudo sh')


@task
@runs_once
def update_minion_config():
    """Updates minion's config and restarts ``salt-minion`` service."""
    put('salt/minion.conf', '/etc/salt/minion', use_sudo=True, mode=0600)

    sudo('chown root:root /etc/salt/minion')

    sudo('service salt-minion restart')


@task
@runs_once
def update_state_and_pillar_files():
    """Updates state and pillar files by uploading them to ``/srv/salt_roots``.
    First it checks whether folder is present. If folder present it will
    be deleted.
    After all ``salt_roots`` folder is uploaded to ``/srv`` and
    owner is changed to root.
    """
    if exists('/srv/salt_roots'):
        sudo('rm -rf /srv/salt_roots')

    upload_project('salt/salt_roots', '/srv', use_sudo=True)

    sudo('chown root:root -R /srv/salt_roots')
    sudo('chmod 600 -R /srv/salt_roots')


@task
@runs_once
def setup_masterless_minion():
    """Prepares server to be able to run Salt commands."""
    bootstrap_salt()
    update_state_and_pillar_files()
    update_minion_config()


@task
@runs_once
def deploy():
    """Deploys infrastructure based on given environment."""
    if env.salt_env_name is None:
        abort('Salt environment has to be specified.')

    update_state_and_pillar_files()

    sudo("salt-call state.highstate env={salt_env_name}".format(
        salt_env_name=env.salt_env_name))









## #########################################################################
## #########################################################################





## TO BE EVALUATED/UPDATED, use with caution
## http://codegists.com/search/fabfile/


from fabric.api import sudo, task, env, local, settings
from fabric.contrib.files import upload_template
from fabric.contrib.project import upload_project

import os


if os.environ.has_key('AS_MASTER_USER'):
    salt_task = hosts('@'.join([os.environ['AS_MASTER_USER'], os.environ['AS_MASTER_HOST']]))
    """Decorator to specify Salt-Stack master user and host."""

@task
def bootstrap_master():
    """Use insecure one-liner to install Salt-Stack master."""
    # XXX: Fails on Docker, see
    # https://github.com/saltstack/salt-bootstrap/issues/394
    with settings(warn_only=True):
        sudo('curl -L http://bootstrap.saltstack.org | sudo sh -s -- -M -N')

    upload_template(
        filename='master.template',
        destination='/etc/salt/master',
        template_dir='config',
        use_sudo=True,
        use_jinja=True,
    )
    sudo('service salt-master restart')


@task
def bootstrap(master_hostname, hostname):
    """Setup salt minion.

    $ fab -H <some_host> bootstrap:<master_hostname>,<some_host_readable_name>
    """
    with settings(warn_only=True):
        sudo('curl -L http://bootstrap.saltstack.org | sudo sh')

    context = {
        'master_hostname': master_hostname,
        'id': hostname,
    }

    upload_template(
        filename='minion.template',
        destination='/etc/salt/minion',
        template_dir='config',
        context=context,
        use_sudo=True,
        use_jinja=True,
    )
    sudo('service salt-minion restart')


@task
def sync_states():
    """Sync Salt-Stack state files."""
    upload_project(local_dir='config/salt', remote_dir='/srv', use_sudo=True)
    upload_project(local_dir='config/pillar', remote_dir='/srv', use_sudo=True)


@task
def master():
    """Run in production."""
    env.user = os.environ['AS_MASTER_USER']
    env.hosts = os.environ['AS_MASTER_HOST']

def saltcmdrun(cmd, *servername_seq):
    """Run salt command on given hosts."""
    args = '-L' if '*' not in servername_seq else ''
    cmd = cmd if cmd else 'cmd.run "uptime"'
    env.output_prefix = False

    sudo('salt {args} "{servername_csv}" {cmd}'.format(
        args=args,
        servername_csv=','.join(servername_seq),
        cmd=cmd,
    ))
