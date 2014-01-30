from fabric.contrib.files import append, exists, sed, run
from fabric.api import env, local, run
import random

REPO_URL = 'https://ropable@bitbucket.org/ropable/tdd-python.git'
SITES_FOLDER = '/var/www'


def deploy():
    _create_directory_structure_if_necessary(env.host)
    source_folder = '{0}/{1}/source'.format(SITES_FOLDER, env.host)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_name):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p {0}/{1}/{2}'.format(SITES_FOLDER, site_name, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {0} && git fetch'.format(source_folder))
    else:
        run('git clone {0} {1}'.format(REPO_URL, source_folder))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd {0} && git reset --hard {1}'.format(source_folder, current_commit))


def _update_database(source_folder):
    run('cd %s && ../virtualenv')
