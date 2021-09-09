from distutils.util import execute
import os
from pathlib import PurePath

from edc_device.constants import CENTRAL_SERVER
from edc_fabric.fabfile.environment import bootstrap_env, update_fabric_env
from edc_fabric.fabfile.files import mount_dmg_locally, dismount_dmg_locally, mount_dmg
from edc_fabric.fabfile.mysql import install_protocol_database
from edc_fabric.fabfile.repositories import get_repo_name
from edc_fabric.fabfile.utils import launch_webserver
from edc_fabric.fabfile.virtualenv.tasks import activate_venv
from fabric.api import task, run, warn, cd, env, local, lcd, put
from fabric.colors import yellow, blue, red
from fabric.contrib.files import exists, sed
from fabric.contrib.project import rsync_project
from fabric.operations import sudo
from fabric.utils import abort

from .prepare_env import prepare_env


@task
def validate(release=None, pull=None):
    """
        fab -H mmathethe utils.validate:release=0.1.24 --user=django
    """
    result = run('source /Users/esr21/.venvs/esr21', warn_only=True)
    if result:
        warn(yellow(f'{env.host}: {result}'))
    else:
        result = run('source /Users/esr21/.venvs/esr21 && python --version', warn_only=True)
        if result != 'Python 3.9.0':
            warn(yellow(f'{env.host}: {result}'))
        else:
            with cd('~/source/esr21'):
                result = run('git tag')
                if release not in result:
                    result = run('git describe --abbrev=0 --tags')
                    warn(
                        yellow(f'{env.host}: esr21 tag not found. Got {result}'))
                    if pull:
                        run('git pull')
            result = run('curl http://localhost')
            if 'Bad Gateway' in result:
                warn(yellow(f'{env.host}: bad gateway'))
            else:
                if not exists('~/media/transactions'):
                    warn(yellow(f'{env.host}: Media folder not ready'))
                else:
                    warn(blue(f'{env.host}: OK'))


@task
def install_protocol_database_task(bootstrap_path=None, bootstrap_branch=None,
                                   release=None, map_area=None, skip_backup=None):
    """Overwrites the client DB.

    For example:

        fab -P -R deploy.install_protocol_database_task:bootstrap_path=/Users/erikvw/source/esr21/fabfile/conf/,release=

    """
    bootstrap_env(
        path=bootstrap_path,
        filename='bootstrap_client.conf',
        bootstrap_branch=bootstrap_branch)
    if not release:
        abort('release not specified')

    update_fabric_env()

    install_protocol_database(skip_backup=skip_backup,
                              release=release)


def update_esr21_conf(project_conf=None, map_area=None):
    """Updates the esr21.conf file on the remote host.
    """
    project_conf = project_conf or env.project_conf
    map_area = map_area or env.map_area
    remote_copy = os.path.join(env.etc_dir, project_conf)
    if not exists(env.etc_dir):
        sudo('mkdir {etc_dir}'.format(etc_dir=env.etc_dir))


def list_tags_from(pip_file=None):
    data = {}
    with open(os.path.expanduser(pip_file), 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line)
            package, tag = line.split('==')
            data.update({package.strip(): tag.strip()})
    return data


@task
def query_tx_task(**kwargs):
    """Check for any host with pending transactions.

    fab -P -R utils.query_tx_task:bootstrap_path=/Users/imosweu/source/esr21/fabfile/conf/  --user=esr21

    """
    prepare_env(**kwargs)

    # run('brew services restart mysql', quiet=True)
    run('mysql -uroot -p edc -Bse \'select  count(*) '
        'from edc_sync_outgoingtransaction where is_consumed_server=0;\' > /tmp/stats1.txt')
    result = run('cat /tmp/stats1.txt')
    if result != '0':
        warn(red(f'{env.host}: pending {result}'))

    run(
        'mysql -uroot -p edc -Bse \'select count(*) '
        'from edc_sync_files_history '
        'where sent=0;\' > /tmp/stats2.txt')
    result = run('cat /tmp/stats2.txt')
    if result != '0':
        warn(red(f'{env.host}: unsent {result}'))


@task
def verify_deployment_db(**kwargs):
    """Generate anonymous transactions.

    fab -P -R mmathethe utils.verify_deployment_db:bootstrap_path=/Users/imosweu/source/bcpp/fabfile/conf/  --user=django

    """
    prepare_env(**kwargs)

    run("mysql -uroot -p edc -Bse \"SELECT COUNT(*) from information_schema.tables "
        "where TABLE_SCHEMA='edc';\"")


def get_pip_freeze_list_from_requirements(requirements_file=None):
    package_names = []
    with cd(env.project_repo_root):
        data = run('cat {requirements}'.format(
            requirements=requirements_file))
        data = data.split('\n')
        for line in data:
            if 'botswana-harvard' in line or 'erikvw' in line:
                repo_url = line.split('@')[0].replace('git+', '')
                tag = line.split('@')[1].split('#')[0]
                package = get_repo_name(repo_url) + '==' + tag
                package_names.append(package)
    return package_names


@task
def check_repo_status(expected_tag=None, **kwargs):
    """Check repo tag.

    fab -P -R mmathethe utils.check_repo_status:bootstrap_path=/Users/imosweu/source/bcpp/fabfile/conf/,expected_tag=0.1.47  --user=django

    """

    prepare_env(**kwargs)

    with cd(os.path.join(env.remote_source_root, env.project_repo_name)):
        if exists('env_dependencies.txt'):
            run('rm env_dependencies.txt')
        run('git checkout master')
        run('source ~/.venvs/bcpp/bin/activate && pip freeze > env_dependencies.txt')
        result = run('git describe --tags')
        if result != expected_tag:
            warn(red(f'master is not at {expected_tag}'))
        data = run('cat env_dependencies.txt')
        data = [d[:-1] for d in data.split('\n')]
        requirements_list = get_pip_freeze_list_from_requirements(
            requirements_file=env.requirements_file)
        for requirement in requirements_list:
            if requirement not in data:
                warn(red(f'{requirement} is not in {env.host}'))


@task
def load_keys_esr21(device_role=None, **kwargs):
    """Load keys for project.

    fab -H azd01 utils.load_keys_bcpp:bootstrap_path=/Users/imosweu/source/esr21/fabfile/conf/,device_role=Client  --user=esr21

    """

    prepare_env(**kwargs)
    # mount dmg
    if device_role == CENTRAL_SERVER:
        mount_dmg_locally(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
                          dmg_passphrase=env.crypto_keys_passphrase)
        if not exists(env.key_path):
            sudo(f'mkdir -p {env.key_path}')
        with lcd(env.key_volume):
            put(local_path='user*',
                remote_path=f'{env.key_path}/', use_sudo=True)
        dismount_dmg_locally(volume_name=env.key_volume)
    else:
        mount_dmg(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
                  dmg_passphrase=env.crypto_keys_passphrase)


@task
def install_dependency_specific_tag(dependency=None, tag=None, account=None, **kwargs):
    """Install a dependency with a specific tag.

    fab -H azd01 utils.install_dependency_specific_tag:bootstrap_path=/Users/imosweu/source/esr21/fabfile/conf/,dependency=esr21-subject,tag=0.1.1, account=covid19-vaccine --user=esr21

    """
    if not account:
        account = 'botswana-harvard'
    egg = '_'.join(dependency.split('-'))
    prepare_env(**kwargs)
    with cd(env.project_repo_root):
        run(f'source {activate_venv()} && pip uninstall {dependency}', warn_only=True)
        run(f'source {activate_venv()} && pip install git+https://github.com/{account}/'
            f'{dependency}.git@{tag}#egg={egg}')


@task
def install_dependency_not_in_requirements(dependency=None, tag=None, **kwargs):
    """Install a dependency with a specific tag.

    fab -H azd01 utils.install_dependency_not_in_requirements:bootstrap_path=/Users/imosweu/source/esr21/fabfile/conf/,dependency=bcpp-subject,tag=0.1.22  --user=django

    """
    prepare_env(**kwargs)
    with cd(env.project_repo_root):
        run(f'source {activate_venv()} && pip uninstall {dependency}', warn_only=True)
        run(f'source {activate_venv()} && pip install {dependency}=={tag}')


@task
def remove_old_sync_files(verify=None, **kwargs):
    """Install a dependency with a specific tag.

    fab -H azd01 utils.remove_old_sync_files:bootstrap_path=/Users/imosweu/source/esr21/fabfile/conf/  --user=esr21

    """
    prepare_env(**kwargs)

    with cd('~/static/'):
        if not verify:
            if exists('edc_sync'):
                run('rm -rf edc_sync')
            if exists('edc_sync_files'):
                run('rm -rf edc_sync_files')
        else:
            if not exists('edc_sync') or not exists('edc_sync_files'):
                print(
                    blue('Missing Edc Sync and Edc Sync Files,'
                         ' folders do not exist.'))


@task
def ssh_copy_id(bootstrap_path=None, use_local_fabric_conf=None, bootstrap_branch=None):
    """
    Example:
        fab -R testhosts -P deploy.ssh_copy_id:config_path=/Users/erikvw/source/esr21/fabfile/,bootstrap_branch=develop,local_fabric_conf=True --user=esr21
    """

    bootstrap_env(
        path=os.path.expanduser(bootstrap_path),
        bootstrap_branch=bootstrap_branch)
    update_fabric_env(use_local_fabric_conf=use_local_fabric_conf)
    pub_key = local('cat ~/.ssh/id_rsa.pub', capture=True)
    with cd('~/.ssh'):
        run('touch authorized_keys')
        result = run('cat authorized_keys', quiet=True)
        if pub_key not in result:
            run('cp authorized_keys authorized_keys.bak')
            run(f'echo {pub_key} >> authorized_keys')


@task
def launch_webserver_esr21_task(**kwargs):
    """Add missing DB column.

    fab -P -R utils.launch_webserver_esr21_task:target_os=Ububtu --user=esr21

    """
    prepare_env(**kwargs)
    launch_webserver()
