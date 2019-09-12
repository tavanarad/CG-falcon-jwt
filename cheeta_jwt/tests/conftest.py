from falcon import testing
import pytest
from cheeta_jwt.tests import api


@pytest.fixture
def client() -> testing.TestClient:
    return testing.TestClient(api)
