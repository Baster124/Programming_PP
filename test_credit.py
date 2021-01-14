import pytest
from flask import json
from werkzeug.security import generate_password_hash, check_password_hash
from package import app, db, engine, client
from package.models import *

from bodies import *



@pytest.fixture
def setup():
    print('setting up')
    db.session.commit()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with open('bodies/users_to_create.json') as u:
        user = json.load(u)
    with open('bodies/login.examples.json') as f:
        log = json.load(f)
    client.post('/user/', json=json.loads(json.dumps(user["1"])))
    client.post('/user/', json=json.loads(json.dumps(user["2"])))
    client.post('/user/', json=json.loads(json.dumps(user["testU"])))
    client.post('/bank/', json=json.loads(json.dumps({"name": "Privat", "budget": 517000})))
    client.post('/bank/', json=json.loads(json.dumps({"name": "Ukrsib", "budget": 10})))
    yield (user, log)

    print("\nClosing database")
    db.session.close()
    db.session.commit()


def login(client, login_info):
    resp = client.post('/login/', json=json.loads(json.dumps(login_info)))
    assert resp.status_code == 200
    json_token = resp.data.decode('utf8').replace("'", '"')
    return json.loads(json_token).get('access_token')


def test_credit_creation(setup):
    user, log = setup
    with open('bodies/credits_to_create.json') as f:
        credit = json.load(f)
    unauth = login(client, log['true_login_data2'])
    resp = client.post('/credit/1', json=json.loads(json.dumps(credit["1"])), headers={'Authorization': 'Bearer ' + unauth})
    assert resp.status_code == 403

    access_token1 = login(client, log['true_login_data1'])
    resp1 = client.post('/credit/1', json=json.loads(json.dumps(credit["1"])),
                        headers={'Authorization': 'Bearer ' + access_token1})
    assert resp1.status_code == 201

    access_token2 = login(client, log['true_login_data2'])
    resp2 = client.post('/credit/2', json=json.loads(json.dumps(credit["2"])),
                        headers={'Authorization': 'Bearer ' + access_token2})
    assert resp2.status_code == 400

    resp3 = client.post('/credit/1', json=json.loads(json.dumps(credit["not_enough_data"])),
                        headers={'Authorization': 'Bearer ' + access_token1})
    assert resp3.status_code == 400


def test_get_credit_by_id(setup):
    user, log = setup
    with open('bodies/credits_to_create.json') as f:
        credit = json.load(f)

    access_token1 = login(client, log['true_login_data1'])
    client.post('/credit/1', json=json.loads(json.dumps(credit["1"])),
                headers={'Authorization': 'Bearer ' + access_token1})
    resp = client.get('/credit/1/1/', headers={'Authorization': 'Bearer ' + access_token1})
    assert resp.status_code == 200

    resp = client.get('/credit/1/2/', headers={'Authorization': 'Bearer ' + access_token1})
    assert resp.status_code == 404

    unauth = login(client, log['true_login_data2'])
    resp = client.get('/credit/2/1/', headers={'Authorization': 'Bearer ' + unauth})
    assert resp.status_code == 403


def test_put_user_by_id(setup):
    user, log = setup
    with open('bodies/credits_to_create.json') as f:
        credit = json.load(f)

    access_token1 = login(client, log['true_login_data1'])
    client.post('/credit/1', json=json.loads(json.dumps(credit["1"])),
                headers={'Authorization': 'Bearer ' + access_token1})
    resp1 = client.put('/credit/1/1/', json=json.loads(json.dumps(credit["data_to_change"])),
                      headers={'Authorization': 'Bearer ' + access_token1})
    assert resp1.status_code == 202

    resp1 = client.put('/credit/1/1/', json=json.loads(json.dumps(credit["empty"])),
                      headers={'Authorization': 'Bearer ' + access_token1})
    assert resp1.status_code == 204

    unauth = login(client, log['true_login_data2'])
    resp2 = client.put('/credit/2/1/', json=json.loads(json.dumps(credit["empty"])),
                      headers={'Authorization': 'Bearer ' + access_token1})
    assert resp2.status_code == 403


def test_for_bank_creation():
    resp_for_bank = client.post('/bank/', json=json.loads(json.dumps({"name": "Privat", "budget": 517000})))
    assert resp_for_bank.status_code == 400
    resp_for_bank = client.post('/bank/', json=json.loads(json.dumps({"name": "Oschad"})))
    assert resp_for_bank.status_code == 400
