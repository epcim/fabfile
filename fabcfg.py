
import os
import yaml

config='fabcfg.yml'

# defaults
environments_default = {
    'region1': {
        'user': 'ubuntu',                           # default user
        #'pass': 'password',                        # default password
        #'gateway': 'root@10.200.50.10',            # gw host, enable only if needed
        'ssh_config_path' : 'ssh_conf.example',     # ssh_conf for env.
        'key_filename' : [                          # list user/access ssh keys
            './id_rsa',
            os.getenv('HOME')+'/.ssh/id_ed25519',
            os.getenv('HOME')+'/.ssh/id_rsa',
        ],
        'hosts': [],
        'roledefs': {                               # define custom groups = roledefs (optional)
            'master': ['cfg01'],
            'mass':   ['mas01'],
        },
    },
    #'region2': { },
    #'dev': { },
    #'test': { },
    #'staging': { },
    #'prod': { },
}


# http://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge/7205107#7205107
def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                #raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
                #override by B (yaml conf)
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a

if os.path.isfile(config):
    environments = yaml.safe_load(open(config))
    #environments = merge(environments_default, environments)
else:
    with open('fabcfg.yml', 'w') as yaml_file:
        yaml.dump(environments_default, yaml_file, default_flow_style=False)

