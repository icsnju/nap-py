from docker import Client

from api.network import Network
from api.volume import Volume
from api.image import Image

from api.exception import NoImage

class Container(object):
    """
    Represents a Docker container
    """

    def __init__(self, url, version, dictionary, volume=None, network=None):
        self.client = Client(base_url=url, version=version)
        self.volume = volume
        self.network = network

        self.options = dictionary

        self.ip = None
        self.id = None
        self.name = None
        self.status = None
        self.image = None
        self.cmd = None
        self.create_time = None
        self.ports = None

    @classmethod
    def get_container(cls, url, version, name):
        cli = Client(base_url=url, version=version)

        containers = cli.containers(all=True)
        for item in containers:
            if '/' + name in item['Names']:

                detail = cli.inspect_container(item['Id'])

                network_name = detail['HostConfig']['NetworkMode']
                network_detail =  cli.inspect_network(network_name)
                network_driver = network_detail['Driver']

                network = Network(network_name, network_driver)
                volume = None

                con = Container(url, version, None, volume, network)

                con.ip = detail['NetworkSettings']['IPAddress']
                con.id = item['Id']
                con.name = name
                con.status = item['Status']
                con.image = item['Image']
                con.cmd = item['Command']
                con.create_time = item['Created']
                con.ports = item['Ports']

                return con

        return None

    def container_exists(cli, name):
        containers = cli.containers(all=True)
        for item in containers:
            if '/' + name in item['Names']:
                return true
        return False

    def create(self):
        params = {}

        if not 'image' in self.options:
            raise NoImage('Container doesnot contain image')

        # params['image'] = Image(self.client, self.options['image'])
        params['image'] = self.options['image']
        self.image = Image(self.client, params['image'])

        if 'command' in self.options:
            params['command'] = self.options['command']

        mem_limit = None
        if 'mem_limit' in self.options:
            # params['mem_limit'] = self.options['mem_limit']
            mem_limit = self.options['mem_limit']

        # ports binding need
        if 'ports' in self.options:
            params['ports'] = self.options['ports']

        if 'environment' in self.options:
            params['environment'] = self.options['environment']

        if 'dns' in self.options:
            params['dns'] = self.options['dns']

        if 'entrypoint' in self.options:
            params['entrypoint'] = self.options['entrypoint']

        if 'cpu_shares' in self.options:
            params['cpu_shares'] = self.options['cpu_shares']

        if 'container_name' in self.options:
            params['name'] = self.options['container_name']

        if 'working_dir' in self.options:
            params['working_dir'] = self.options['working_dir']

        if 'domainname' in self.options:
            params['domainname'] = self.options['domainname']

        if 'mac_address' in self.options:
            params['mac_address'] = self.options['mac_address']

        if not self.network == None:
            network_mode = self.network.name

        binds = None
        if not self.volume.vol == None:
            binds = self.volume.vol

        privileged = False
        if 'privileged' in self.options:
            privileged = self.options['privileged']

        volumes_from = None
        if 'volumes_from' in self.options:
            volumes_from = self.options['volumes_from']

        params['host_config'] = self.client.create_host_config(network_mode=network_mode, binds=binds, privileged=privileged, volumes_from=volumes_from, mem_limit=mem_limit)

        container = self.client.create_container(**params)

        self.id = container.get('Id')

    def start(self):
        self.client.start(container=self.id)

        detail = self.client.inspect_container(container=self.id)

        self.name = detail['Name']
        self.status = detail['State']['Status']

        command = ""
        for item in detail['Config']['Cmd']:
            command = command + item + " "
        self.command = command

        self.create_time = detail['Created']
        self.ip = detail['NetworkSettings']['IPAddress']
        self.ports = detail['NetworkSettings']['Ports']

    @classmethod
    def create_container(cls, url, image, command, name=None, version='1.21', volume=None, network=None):
        cli = Client(base_url=url, version=version)

        params = {
            'image': image,
            'command': command,
                 }

        if not name == None:
            params['name'] = name

        if not network == None:
            params['host_config'] = cli.create_host_config(network_mode=network.name)

        # print params

        container = cli.create_container(**params)
        cli.start(container=container.get('Id'))

        detail = cli.inspect_container(container=container)

        dic = {}
        dic['id'] = detail['Id']
        dic['name'] = detail['Name']
        dic['status'] = detail['State']['Status']
        dic['image'] = image
        dic['cmd'] = command
        dic['create_time'] = detail['Created']
        dic['ip'] = detail['NetworkSettings']['IPAddress']
        dic['ports'] = detail['NetworkSettings']['Ports']

        return cls(cli, volume, network, dic)

    def stop(self):
        self.client.stop(container=self.id)

    def pause(self):
        self.client.pause(container=self.id)

    def unpause(self):
        self.client.unpause(container=self.id)

    def kill(self):
        self.client.kill(container=self.id)

    def remove(self):
        self.client.remove_container(container=self.id)

    def restart(self):
        self.client.restart(container=self.id)
