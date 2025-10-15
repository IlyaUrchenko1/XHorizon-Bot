from prometheus_fastapi_instrumentator import Instrumentator

instrumentator = Instrumentator()

def setup_instrumentator(app):
    instrumentator.instrument(app).expose(app, endpoint="/metrics")
