class NoImage(Exception):
    """
    Represents a container settings without image
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__():
        return self.msg