from gevent import queue


class QueueContainer(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            self = super(QueueContainer, cls).__new__(cls, *args, **kwargs)
            QueueContainer.__init__(self, *args, **kwargs)
            cls._instance = self
        return cls._instance

    def __repr__(self):
        return "{}: {}".format(id(self._container), str(self._container))

    def __init__(self, *args, **kwargs):
        self._container = {'Test Chat Room 1': {'generic': queue.Queue(), }, }

    def __setitem__(self, key, value):
        self._container[key] = value

    def __getitem__(self, key):
        return self._container[key]

    def __delitem__(self, key):
        del self._container[key]
