import os

from aioamqp.channel import Channel
from waspy import Application, Config
from waspy.transports import HTTPToolsTransport, RabbitMQTransport

from . import middlewares
from .controllers import echo
from .controllers import foo
from .controllers import other


CONFIG_LOCATION = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'config.yaml')


async def on_start(app):
    # channel: Channel = rabbit.channel
    # channel.exchange_bind('amq.headers', '')
    # channel.queue_bind('foo', 'amq.headers', arguments={'x-match': "all", })
    pass


def add_routes(app):
    app.router.add_get('/', other.ping)
    app.router.add_get('/ping', other.ping)
    app.router.add_get('/error', other.error)
    app.router.add_post('/callback', other.callback)
    app.router.add_get('/echo', echo.echo_request)
    app.router.add_post('/echo', echo.echo_body)
    app.router.add_get('/foo/{id}', foo.foo_get)
    app.router.add_put('/foo/{id}', foo.foo_put)
    app.router.add_post('/foo', foo.foo_post)
    app.router.add_delete('/foo/{id}', foo.foo_delete)
    app.router.add_patch('/foo/{id}', foo.foo_patch)
    app.router.add_get('/large', other.large)


def get_app():
    config = Config().from_file(CONFIG_LOCATION)

    http = HTTPToolsTransport(port=config['http']['port'], prefix='',
                              shutdown_grace_period=2,
                              shutdown_wait_period=15)


    rabbit = RabbitMQTransport(
        url=config['rabbitmq']['url'],
        port=config['rabbitmq']['port'],
        queue=config['rabbitmq']['queue'],
        virtualhost=config['rabbitmq']['virtualhost'],
        username=config['rabbitmq']['username'],
        password=config['rabbitmq']['password'],
        ssl=config['rabbitmq']['ssl'],
        verify_ssl=config['rabbitmq']['verify_ssl']
    )

    middlewares_ = [
        middlewares.attach_object,
        middlewares.add_header
    ]

    app = Application(transport=(http),
                      middlewares=middlewares_,
                      default_headers={'Server': 'foo-service'},
                      config=config)

    app.on_start.append(on_start)

    add_routes(app)

    return app


def main():
    app = get_app()
    app.run()


