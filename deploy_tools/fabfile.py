from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'git@bitbucket.org:ropable/tdd-python.git'
SITES_FOLDER = '/var/www'


def deploy():
    # env.host will contain the address of the host that we
    # specify at the command line, e.g.:
    # fab deploy:host=superlists-staging
    _create_directory_structure_if_necessary(env.host)
    source_folder = '{0}/{1}/source'.format(SITES_FOLDER, env.host)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_name):
    for subfolder in ('database', 'static', 'virtualenv', 'source', 'logs'):
        run('mkdir -p {0}/{1}/{2}'.format(SITES_FOLDER, site_name, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {0} && git fetch'.format(source_folder))
    else:
        run('git clone {0} {1}'.format(REPO_URL, source_folder))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd {0} && git reset --hard {1}'.format(source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(
        settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["{0}"]'.format(site_name)
    )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):  # 3
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3.3 {0}'.format(virtualenv_folder))
    run('{0}/bin/pip install -r {1}/requirements.txt'.format(
        virtualenv_folder, source_folder))


def _update_static_files(source_folder):
    run('cd {0} && ../virtualenv/bin/python3 manage.py collectstatic --noinput'.format(
        source_folder))


def _update_database(source_folder):
    run('cd {0} && ../virtualenv/bin/python manage.py syncdb --migrate --noinput'.format(
        source_folder))
