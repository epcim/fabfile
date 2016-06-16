# fabfile
Handy Fabric collection to avoid manually ssh to remote. 

## Usage
Clone as "fabfile" to your project.

## Documentation

Use native fabric comands

  fab --list
  fab --list-format=nested --list

  # some modules may print some tips
  fab salt.help


For more info have a look on documentation:
- http://wiki.fabfile.org/Recipes
- http://docs.fabfile.org/en/1.4.3/#api-documentation


## Aka 'modules':
 - ops.py  - Common sysadmin operations
 - salt.py - Fabric for saltstack. Salt operations, to be run on your workstation in your beloved shell environment
