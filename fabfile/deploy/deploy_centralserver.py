from fabric.api import task

from .deploy import deploy


@task
def deploy_centralserver(**kwargs):
    """

        fab -H esr21 deploy.deploy_centralserver:bootstrap_path=/Users/imosweu/source/esr21/fabfile/conf/,release=0.1.1, --user=django

    """

    conf_filename = 'bootstrap_centralserver.conf'
    deploy(conf_filename=conf_filename, **kwargs)
