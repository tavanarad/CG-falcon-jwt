import falcon


def test_decode_jwt(client):
    result = client.simulate_get('/UserResource')
    assert result.status == falcon.HTTP_200

    result = client.simulate_post('/UserResource', body=b'fake_data')
    assert result.status == falcon.HTTP_401

    headers = {
        "AUTHORIZATION": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoxMjN9.65dc0yDsOFVxrqGCSNaoqhxLVVldKf8L1SHJ4nFTvRw"
    }

    result = client.simulate_post('/UserResource', body=b'fake_data', headers=headers)
    assert result.status == falcon.HTTP_200
    assert result.json == 123

    headers = {
        "AUTHORIZATION": "Bearer e1yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoxMjN9.65dc0yDsOFVxrqGCSNaoqhxLVVldKf8L1SHJ4nFTvRw"
    }

    result = client.simulate_put('/UserResource', body={}, json=headers)
    assert result.status == falcon.HTTP_401
    assert result.json != 1234
