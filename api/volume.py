

class Volume(object):
    """
    Represents a volume in nap
    """

    # vol is a list ['host_path:container/path:rw', '/home:/var:ro']
    def __init__(self, vol):
        self.vol = vol
