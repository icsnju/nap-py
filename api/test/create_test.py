from api.container import Container
from api.network import Network

from api.exception import NoImage

def create_container_test():
    net = Network(name='test', driver='bridge')

    container = Container.create_container(network=net, name='ttttt', url='114.212.87.52:2376', image='ubuntu', command='/bin/sleep 30', version='1.21')
    print container.ip
    print container.cmd
    print container.ports

def create_noimage():
    url = '114.212.87.52:2376'
    version = '1.21'
    volume = None
    network = None

    dic = {}
    dic['container_name'] = 'test'

    con = Container(url, version, dic, volume, network)
    con.create()

if __name__ == '__main__':
    try:
        create_noimage()
    except NoImage as e:
        print e.msg
