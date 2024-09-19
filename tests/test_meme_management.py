import sys
import os
import pytest
import requests


def test_get_meme_by_id(get_meme_by_id_endpoint, meme_req_id, meme_user):
    token = meme_user.get_token()
    get_meme_by_id_endpoint.get_meme_by_id(meme_req_id, token=token)
    get_meme_by_id_endpoint.check_that_status_is_200()


def test_get_all_meme(get_all_meme_endpoint, meme_user):
    token = meme_user.get_token()
    get_all_meme_endpoint.get_all_meme(token=token)
    get_all_meme_endpoint.check_that_status_is_200()


def test_get_meme_by_non_existing_id(get_meme_by_id_endpoint, non_existent_id, meme_user):
    token = meme_user.get_token()
    get_meme_by_id_endpoint.get_meme_by_id(non_existent_id, token=token)
    get_meme_by_id_endpoint.check_that_status_is_404()


def test_get_meme_without_authorization(get_meme_by_id_endpoint, meme_req_id, meme_user):
    token = meme_user.get_token()
    get_meme_by_id_endpoint.get_meme_by_id(meme_req_id, token=None)
    get_meme_by_id_endpoint.check_that_status_is_401()


def test_add_meme(create_meme_endpoint, data, meme_user):
    token = meme_user.get_token()
    create_meme_endpoint.create_new_meme(payload=data, token=token)
    create_meme_endpoint.check_that_status_is_200()
    create_meme_endpoint.check_response_text_is_correct(data["text"])
    create_meme_endpoint.check_response_url_is_correct(data["url"])
    create_meme_endpoint.check_response_tags_is_correct(data["tags"])
    create_meme_endpoint.check_response_info_is_correct(data["info"])


def test_add_meme_missing_fields(create_meme_endpoint, data_incomplete, meme_user):
    token = meme_user.get_token()
    create_meme_endpoint.create_new_meme(payload=data_incomplete, token=token)
    create_meme_endpoint.check_that_status_is_400()


def test_add_meme_with_invalid_url(create_meme_endpoint, data_invalid_url, meme_user):
    token = meme_user.get_token()
    create_meme_endpoint.create_new_meme(payload=data_invalid_url, token=token)
    create_meme_endpoint.check_that_status_is_400()


def test_add_meme_with_large_payload(create_meme_endpoint, data_large_payload, meme_user):
    token = meme_user.get_token()
    create_meme_endpoint.create_new_meme(payload=data_large_payload, token=token)
    create_meme_endpoint.check_that_status_is_200()
    create_meme_endpoint.check_that_status_is_200()
    create_meme_endpoint.check_response_text_is_correct(data_large_payload["text"])
    create_meme_endpoint.check_response_url_is_correct(data_large_payload["url"])
    create_meme_endpoint.check_response_tags_is_correct(data_large_payload["tags"])
    create_meme_endpoint.check_response_info_is_correct(data_large_payload["info"])


def test_update_meme(update_meme_endpoint, meme_id):
    payload = {
        "id": meme_id,
        "text": "When you saved money and skipped QA",
        "url": "https://mailtrap.io/wp-content/uploads/2020/06/testing_meme4.jpg",
        "tags": ["fun", "QA"],
        "info": {"colors": ["orange", "grey", "white"], "objects": ["picture", "text"]}}
    update_meme_endpoint.update_meme(meme_id, payload)
    update_meme_endpoint.check_that_status_is_200()
    update_meme_endpoint.check_response_text_is_correct(payload["text"])
    update_meme_endpoint.check_response_url_is_correct(payload["url"])
    update_meme_endpoint.check_response_tags_is_correct(payload["tags"])
    update_meme_endpoint.check_response_info_is_correct(payload["info"])


def test_update_non_existent_meme(update_meme_endpoint, non_existent_id, data_invalid_meme_id):
    update_meme_endpoint.update_meme(non_existent_id, payload=data_invalid_meme_id)
    update_meme_endpoint.check_that_status_is_404()


def test_update_meme_with_no_changes(update_meme_endpoint, meme_id, meme_user):
    payload = {
        "id": meme_id,
        "text": "When you saved money and skipped QA",
        "url": "https://mailtrap.io/wp-content/uploads/2020/06/testing_meme4.jpg",
        "tags": ["fun", "QA"],
        "info": {"colors": ["orange", "grey", "white"], "objects": ["picture", "text"]}
    }
    token = meme_user.get_token()
    update_meme_endpoint.update_meme(meme_id, payload, token=token)
    update_meme_endpoint.check_that_status_is_200()
    update_meme_endpoint.check_response_text_is_correct(payload["text"])
    update_meme_endpoint.check_response_url_is_correct(payload["url"])
    update_meme_endpoint.check_response_tags_is_correct(payload["tags"])
    update_meme_endpoint.check_response_info_is_correct(payload["info"])


def test_delete_meme(delete_meme_endpoint, meme_id, meme_user):
    token = meme_user.get_token()
    delete_meme_endpoint.delete_meme(meme_id)
    delete_meme_endpoint.check_that_status_is_200()
    delete_meme_endpoint.check_if_meme_deleted()
    delete_meme_endpoint.check_status_of_deleted_meme(meme_id)


def test_delete_non_existing_meme(delete_meme_endpoint, non_existent_id, meme_user):
    token = meme_user.get_token()
    delete_meme_endpoint.delete_meme(non_existent_id)
    delete_meme_endpoint.check_that_status_is_404()
