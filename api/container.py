from docker import Client

from api.network import Network
from api.volume import Volume
from api.exception import NoImage

class Container(object):
    """
    Represents a Docker container
    """

    def __init__(self, client, version, volume, network, dictionary):
        self.client = Client(base_url=client, version=version)
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

    def create(self):
        params = {}

        if not 'image' in self.options:
            raise NoImage('Container doesnot contain image')

        params['image'] = self.options['image']
        self.image = params['image']

        if 'container_name' in self.options:
            params['name'] = self.options['container_name']
        
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

    def stop(timeout=0):
        self.client.stop(container=self.name, timeout=timeout)

    def remove():
        self.client.remove_container(container=self.name)
