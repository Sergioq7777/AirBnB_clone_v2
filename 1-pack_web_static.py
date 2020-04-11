#!/usr/bin/python3
'''script that generates a .tgz archive from the contents of the web_static'''
from fabric.api import local
from datetime import datetime
from os.path import exists
from os import makedirs


def do_pack():
    '''Packs files'''
    if not exists('versions'):
        makedirs('versions')
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filepath = 'versions/web_static_' + timestamp + '.tgz'
    local('tar cvfz ' + filepath + ' web_static')
    if exists(filepath):
        return filepath
    else:
        return None
