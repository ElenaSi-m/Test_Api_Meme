import pytest
from endpoints.get_meme import GetMeme
from endpoints.get_all_meme import GetAllMeme
from endpoints.create_meme import CreateMeme
from endpoints.meme_user import MemeUser
from endpoints.update_meme import UpdateMeme
from endpoints.delete_meme import DeleteMeme


@pytest.fixture()
def get_all_meme_endpoint():
    return GetAllMeme()


@pytest.fixture()
def get_meme_by_id_endpoint():
    return GetMeme()


@pytest.fixture()
def create_meme_endpoint():
    return CreateMeme()


@pytest.fixture()
def meme_user():
    user = MemeUser()
    user.on_start()
    return user


@pytest.fixture()
def meme_req_id():
    return 1


@pytest.fixture()
def data():
    return {
        "text": "Devs skipped QA",
        "url": "https://mailtrap.io/wp-content/uploads/2020/06/testing_meme4.jpg",
        "tags": ["fun", "QA"], "info": {"colors": ["orange", "grey", "white"], "objects": ["picture", "text"]}}


@pytest.fixture()
def data_invalid_url():
    return {
        "text": "Meme with invalid url",
        "url": 444,
        "tags": ["invalid"],
        "info": {"colors": ["purple"], "objects": ["text"]}
    }


@pytest.fixture()
def data_incomplete():
    return {
        "text": "Incomplete meme",

    }


@pytest.fixture()
def data_invalid_meme_id():
    non_existent_id = 999999
    return {
        "id": non_existent_id,
        "text": "Updated meme with invalid id",
        "url": "https://mailtrap.io/wp-content/uploads/2020/06/testing_meme4.jpg",
        "tags": ["invalid"],
        "info": {"colors": ["red"], "objects": ["text"]}
    }


@pytest.fixture()
def data_large_payload():
    return {
        "text": "Large payload test",
        "url": "https://example.com/large_image.jpg",
        "tags": ["large", "payload"],
        "info": {
            "colors": ["red"] * 500,
            "objects": ["object"] * 500
        }
    }


@pytest.fixture()
def non_existent_id():
    return 999999


@pytest.fixture()
def update_meme_endpoint():
    return UpdateMeme()


@pytest.fixture()
def meme_id(create_meme_endpoint, data, meme_user, delete_meme_endpoint):
    token = meme_user.get_token()
    print(f"Token: {token}")
    print(f"Payload: {data}")
    response = create_meme_endpoint.create_new_meme(payload=data, token=token)
    print(f"Create meme response: {response}")

    create_meme_endpoint.create_new_meme(data)

    yield create_meme_endpoint.meme_id
    delete_meme_endpoint.delete_meme(create_meme_endpoint.meme_id)
    delete_meme_endpoint.check_status_of_deleted_meme(create_meme_endpoint.meme_id)


@pytest.fixture()
def delete_meme_endpoint():
    return DeleteMeme()


@pytest.fixture(scope="function")
def cleanup(create_meme_endpoint, delete_meme_endpoint):
    yield
    # Cleanup any resources
    if create_meme_endpoint.meme_id:
        delete_meme_endpoint.delete_meme(create_meme_endpoint.meme_id)
        delete_meme_endpoint.check_status_of_deleted_meme(create_meme_endpoint.meme_id)
