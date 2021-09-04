from fabric.api import task
from .deploy import deploy


@task
def deploy_client(*requirements_list, **kwargs):
    """Deploy clients from the deployment host.

    Assumes you have already prepared the deployment host

    Will use conf files on deployment

    For example:

    Copy ssh keys:

        fab -P -R mmankgodi deploy.ssh_copy_id:bootstrap_path=/Users/imosweu/source/bcpp/fabfile/conf,bootstrap_branch=develop --user=esr21

    Deploy:

        fab -H azd01 deploy.deploy_client:bootstrap_path=/Users/imosweu/source/esr21/fabfile/conf/,release=0.1.1,--user=esr21

    - OR -

        fab -P -R mmankgodi deploy.deploy_client:bootstrap_path=/Users/imosweu/source/esr21/fabfile/conf/,release=0.1.1, --user=esr21

    Once complete:

        fab -P -R mmankgodi deploy.validate:release=0.1.1 --user=esr21

    """
    conf_filename = 'bootstrap_client.conf'
    deploy(requirements_list=requirements_list,
           conf_filename=conf_filename, **kwargs)
