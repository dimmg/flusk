from ..models import Foss


def test_create_foss_implicitly():
    payload = {
        'name': 'foss',
        'email': 'foss@example.com'
    }

    foss = Foss(**payload)
    foss.save()

    assert foss.email == payload['email']


def test_create_foss_with_session(session):
    payload = {
        'name': 'bar',
        'email': 'bar@example.com'
    }

    foss = Foss(**payload)
    session.add(foss)
    session.flush()

    assert foss.name == payload['name']
