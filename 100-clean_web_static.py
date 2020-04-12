#!/usr/bin/python3
'''Fabric script that distributes an archive to a remote server'''
from fabric.api import local, env, put, run, runs_once
from datetime import datetime
from os.path import exists, isfile
from os import makedirs

env.hosts = ['35.185.114.101', '35.185.47.103']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/holberton'


@runs_once
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


def do_deploy(archive_path):
    '''Deploys archive web servers'''
    if not exists(archive_path) and not isfile(archive_path):
        return False
    try:
        put(archive_path, '/tmp')
        filename = archive_path.split('/')[1][:-4]
        run('sudo mkdir -p /data/web_static/releases/' + filename + '/')
        run('sudo chown -R ubuntu:ubuntu /data')
        run('tar -xzf /tmp/' + filename + '.tgz'
            ' -C /data/web_static/releases/' + filename + '/')
        run('rm /tmp/' + filename + '.tgz')
        run('mv /data/web_static/releases/' + filename + '/web_static/* ' +
            '/data/web_static/releases/' + filename + '/')
        run('rm -rf /data/web_static/releases/' + filename + '/web_static')
        run('rm -rf /data/web_static/current')
        run('ln -sf /data/web_static/releases/' + filename + '/ ' +
            '/data/web_static/current')
        return True
    except:
        return False
    return True


def deploy():
    '''Runs do_pack and do_deploy'''
    filepath = do_pack()
    if filepath:
        exit_status = do_deploy(filepath)
        return exit_status
    else:
        return False


def do_clean(number=0):
    '''Cleans excess archives on local and remote'''
    number = int(number)
    if number == 0:
        number = 1
    keep = local('ls -1t versions', capture=True).split('\n')[:number]
    clean_local(keep)
    keep = [f[:-4] for f in keep]
    tmp = run('ls -1 /data/web_static/releases').split('\n')
    filelist = [f.strip('\r') for f in tmp]
    for f in filelist:
        if f not in keep:
            run('rm -rf /data/web_static/releases/{}'.format(f))


@runs_once
def clean_local(keep):
    '''Cleans local archives'''
    filelist = local('ls -1 versions', capture=True).split('\n')
    for f in filelist:
        if f not in keep:
            local('rm versions/{}'.format(f))
