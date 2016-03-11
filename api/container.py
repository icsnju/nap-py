from docker import Client

from api.network import Network
from api.volume import Volume

class Container(object):
    """
    Represents a Docker container
    """

    def __init__(self, client, volume, network, dictionary):
        self.client = client
        self.volume = volume
        self.network = network

        self.ip = dictionary["ip"]
        self.id = dictionary['id']
        self.name = dictionary['name']
        self.status = dictionary['status']
        self.image = dictionary['image']
        self.cmd = dictionary['cmd']
        self.create_time = dictionary['create_time']
        self.ports = dictionary['ports']

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
