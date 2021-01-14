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

    yield (user, log)
    print("\nClosing database")
    db.session.close()
    db.session.commit()


def test_login(setup):
    user, log = setup
    resp = client.post('/login/', json=json.loads(json.dumps(log['true_login_data'])))
    assert resp.status_code == 200
    resp1 = client.post('/login/', json=json.loads(json.dumps(log["incorrect_pas"])))
    assert resp1.status_code == 401
    resp2 = client.post('/login/', json=json.loads(json.dumps(log["only_username"])))
    assert resp2.status_code == 400
    resp2 = client.post('/login/', json=json.loads(json.dumps(log["only_pass"])))
    assert resp2.status_code == 400
    resp2 = client.post('/login/', json=json.loads(json.dumps(log["test_data"])))
    assert resp2.status_code == 404


def login(client, login_info):
    try:
        resp = client.post('/login/', json=json.loads(json.dumps(login_info)))
        assert resp.status_code == 200
        json_token = resp.data.decode('utf8').replace("'", '"')
        return json.loads(json_token).get('access_token')
    except Exception as e:
        assert resp.status_code == 404


def test_user_create(setup):
    with open('bodies/users_to_create.json') as u:
        user = json.load(u)
    resp = client.post('/user/', json=json.loads(json.dumps(user["3"])))
    assert resp.status_code == 201
    assert resp.json["data"]["username"] == user["3"]["username"]
    assert resp.json["data"]["firstname"] == user["3"]["firstname"]
    assert resp.json["data"]["lastname"] == user["3"]["lastname"]
    assert check_password_hash((resp.json["data"]["password"]), user["3"]["password"])

    resp1 = client.post('/user/', json=json.loads(json.dumps(user["3"])))
    assert resp1.status_code == 400
    resp1 = client.post('/user/', json=json.loads(json.dumps(user["bad_data"])))
    assert resp1.status_code == 400


def test_get_user_by_id(setup):
    user, log = setup
    access_token = login(client, log['true_login_data1'])
    resp = client.get('/user/1', headers={'Authorization': 'Bearer ' + access_token})
    assert resp.status_code == 200

    unauth = login(client, log['true_login_data2'])
    resp = client.get('/user/1', headers={'Authorization': 'Bearer ' + unauth})
    assert resp.status_code == 403
    not_exists = login(client, log['test_data'])


def test_put_user_by_id(setup):
    user, log = setup
    access_token = login(client, log['true_login_data1'])
    resp = client.put('/user/1', json=json.loads(json.dumps(user["data_to_change"])),
                      headers={'Authorization': 'Bearer ' + access_token})
    assert resp.status_code == 202

    resp = client.put('/user/1', json=json.loads(json.dumps(user["empty"])),
                      headers={'Authorization': 'Bearer ' + access_token})
    assert resp.status_code == 204

    unauth = login(client, log['true_login_data2'])
    resp = client.get('/user/1', json=json.loads(json.dumps(user["data_to_change"])),
                      headers={'Authorization': 'Bearer ' + unauth})
    assert resp.status_code == 403
    not_exists = login(client, log['test_data'])


def test_delete_user_by_id(setup):
    user, log = setup
    unauth = login(client, log['true_login_data2'])
    resp = client.delete('/user/1', headers={'Authorization': 'Bearer ' + unauth})
    assert resp.status_code == 403

    access_token = login(client, log['true_login_data1'])
    resp = client.delete('/user/1', headers={'Authorization': 'Bearer ' + access_token})
    assert resp.status_code == 200

    access_token = login(client, log['true_login_data1'])
