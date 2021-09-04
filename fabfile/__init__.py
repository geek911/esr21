import sys

if 'fab' in sys.argv[0]:
    from edc_fabric import fabfile as common
    from .deploy import (
        deploy_centralserver, deploy_client, deploy_nodeserver, deployment_host)
    from .local_base_env import load_base_env
    # from .utils import (
        # load_keys_esr21, check_repo_status, install_dependency_specific_tag,
        # install_dependency_not_in_requirements)

    load_base_env()
