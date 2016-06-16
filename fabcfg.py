
import os
from fabric.api import *

environments = {
    'test': {
        'user': 'root',
        'pass': 'password',
        'gateway': '',
        'key_filename' : [
            os.getenv('HOME')+'/.ssh/id_dsa',
            os.getenv('HOME')+'/.ssh/id_ed25519'
        ],
        'ssh_config_path' : '',
        'hosts': [],
        'roledefs': {
            'master': [],
            'control': [],
            'kvm': [],
        },
    },
    #'dev': { },
}



