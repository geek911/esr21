def get_gaborone():
    hosts = ['azd0{}'.format(i) for i in range(1, 11)]
    return hosts


roledefs = {
    'deployment_hosts': ['localhost'],
    'gaborone': get_gaborone(),
    'testhosts': ['nimrod', 'moses'],
}
