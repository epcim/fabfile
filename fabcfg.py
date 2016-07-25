
import os
#from fabric.api import *


environments = {
    'st': {
        #'user': 'root',                                             # default user
        #'pass': 'password',                                         # default password
        'gateway': 'root@10.171.20.50',                              # enable only if needed
        'ssh_config_path' : 'fabfile/config/slovaktelekom_poc.conf', # hosts to be resolved from fabric
        'key_filename' : [                                           # list user/access ssh keys
            os.getenv('HOME')+'/.ssh/id_dsa',
            os.getenv('HOME')+'/.ssh/id_ed25519'
        ],
        'hosts': [],
        'roledefs': {                                                # define custom groups = roledefs (optional)
            'master': ['cfg01'],
            'mass': ['mas01'],
            'ctl': ['ctl01', 'ctl02', 'ctl03'],
            'cmp': [#'cmp01', 'cmp02',
                    'cmp03','cmp04','cmp05'],
            'kvm': ['kvm01', 'kvm02', 'kvm03'],
            # 'web': ['web01'],
            # 'mon': ['mon01'],
            # 'mtr': ['mtr01'],
            # 'dbs': ['dbs01', 'dbs02', 'dbs03'],
            # 'mdb': ['mdb01', 'mdb02', 'mdb03'],
            # 'prx': ['prx01', 'prx02'],
            # 'mtr': ['mtr01', 'mtr02'],
            # 'mon': ['mon01'],
            # 'bil': ['bil01'],
        },
    },
    #'dev': { },
}


# TODO, if exist __file__.yml then load yml and replace cfg in environments dict.





