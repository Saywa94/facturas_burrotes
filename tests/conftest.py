import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app

app = create_app()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
