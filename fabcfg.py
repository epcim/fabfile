
import os
from fabric.api import *


environments = {
    'vpc20': {
        'user': 'root',
        'pass': 'password',
        'gateway': '10.10.15.3',
        'key_filename' : [
            os.getenv('HOME')+'/.ssh/id_dsa',
            os.getenv('HOME')+'/.ssh/id_ed25519'
        ],
        'ssh_config_path' : 'fabfile/config/vpc20.conf',
        'hosts': [],
        'roledefs': {
        # TODO, autopopulate/update methods (ie: from salt registered nodes)
        # read configs, etc..
            'master': ['cfg01'],
            #'mass': ['mas01'],
            'ctl': ['ctl01', 'ctl02', 'ctl03'],
            'cmp': ['cmp01', 'cmp02'],
            'web': ['web01'],
            'mon': ['mon01'],
            'mtr': ['mtr01'],
            #'kvm': ['kvm01', 'kvm02', 'kvm03'],
            #'dbs': ['dbs01', 'dbs02', 'dbs03'],
            #'mdb': ['mdb01', 'mdb02', 'mdb03'],
            #'prx': ['prx01', 'prx02'],
            #'mtr': ['mtr01', 'mtr02'],
            #'mon': ['mon01'],
            #'bil': ['bil01'],
        },
    },
    #'dev': { },
}



