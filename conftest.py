import os
import pytest

@pytest.fixture(scope="session")
def api_url():
    return os.getenv("API_URL", "http://127.0.0.1:5000")
