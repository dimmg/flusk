import json


def test_create_foss(test_client, custom_headers):
    payload = {
        'name': 'foo',
        'email': 'bar@foo.com'
    }
    r = test_client.post('/foss', data=json.dumps(payload),
                         headers=custom_headers)

    assert r.status_code == 200
