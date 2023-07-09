from prometheus_client import Counter


class Metric:

    def __init__(self, params: list = ['client', 'path', 'full_path']) -> None:
        self.user = Counter('user', 'Proxy', params)

    def register_user(self, params):
        self.user.labels(**params).inc()


metric = Metric()
