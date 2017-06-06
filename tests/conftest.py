import pytest

from waspy.transports import TestTransport

from app.core import get_app


@pytest.fixture
def transport():
    transport_ = TestTransport()
    app_ = get_app()
    transport_.run_app(app_)
    return transport_
