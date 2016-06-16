# fabfile
Handy Fabric collection to avoid manually ssh to remote. 

## Usage
Clone as "fabfile" to your project.

## Documentation

Use native fabric comands
```
  fab --list
  fab --list-format=nested --list
```
```
  # some modules may print some tips
  fab salt.help
```

For more info have a look on documentation:
- http://wiki.fabfile.org/Recipes
- http://docs.fabfile.org/en/1.4.3/#api-documentation

# Aka 'modules':

 - ops.py  - Common sysadmin operations
 - salt.py - Fabric for saltstack. Salt operations, to be run on your workstation in your beloved shell environment


## Ops

### Usage examples

```
fab setenv:prod push_key:~/tmp/admin_id_dsa.pub,user='root'
```


## Salt

### shell shortcuts

```
function fabsalt()    { action=$1;shift;X=$@; fab salt.$action:"${X//\*/\*}" };
function control()    { X=$@; fab salt.cmd:hosts='ctl01',"source /root/keystonerc;${X//\*/\*}" }
function compute()    { X=$@; fab salt.cmd:hosts='cmp01',"source /root/keystonerc;${X//\*/\*}" }
function smaster()    { X=$@; fab salt.cmd:role='master',"${X//\*/\*}" }
alias salt="fabsalt salt";
alias salt-key="fabsalt key";
alias salt-call="fabsalt call";
alias salt-cmd="fabsalt cmd";
```

### Usage examples
```

fab -H ctl01 salt.call:"state.sls linux"
fab -H ctl01 salt.cmd:contrail-status
fab salt.call:"state.sls linux",roles=ctl
fab -g 10.10.15.3 --skip-bad-hosts setenv:vpc20 salt.cmd:"hostname -I"

saltmaster salt 'ctl*' service.restart nova-api
control salt-call state.highstate
compute salt-call state.highstate

salt-cmd contrail status
salt-cmd salt 'ctl*' service.restart nova-api

salt ctl\* grains.get ipv4
salt ctl\* state.highstate
salt \* state.highstate
salt \* cmd.exec_code python \'import sys\; print sys.version\'

```

 

