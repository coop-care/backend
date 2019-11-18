import connexion
import pytest


@pytest.fixture(scope='module')
def test_client():
    appl = connexion.App(__name__)
    appl.add_api('openapi.yaml', validate_responses=True) 
    # Establish an application context before running the tests.
    ctx = appl.app.app_context()
    ctx.push()
    yield appl.app.test_client()  # this is where the testing happens!
    ctx.pop()

def test_app_client_problems(test_client):
    assert test_client.get('/v0/client/1/problems').status_code == 200

def test_omaha_intervention_categories(test_client):
    assert test_client.get('/v0/omaha/intervention_categories').status_code == 200

def test_omaha_intervention_targets(test_client):
    assert test_client.get('/v0/omaha/intervention_targets').status_code == 200

def test_omaha_problem_domains(test_client):
    assert test_client.get('/v0/omaha/problem_domains').status_code == 200

def test_omaha_problems(test_client):
    assert test_client.get('/v0/omaha/problems').status_code == 200

def test_omaha_symptoms(test_client):
    assert test_client.get('/v0/omaha/symptoms').status_code == 200