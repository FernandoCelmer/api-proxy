from prometheus_client import Counter


class Metric:

    def __init__(self, params: list = ['client', 'path']) -> None:
        self.get = Counter('get', 'Proxy', params)
        self.post = Counter('post', 'Proxy', params)
        self.put = Counter('put', 'Proxy', params)
        self.patch = Counter('patch', 'Proxy', params)
        self.delete = Counter('delete', 'Proxy', params)

    def register(self, method, params):
        getattr(self, method).labels(**params).inc()
