import pytest
import requests
import json

base_url = 'http://127.0.0.1:8000/'
register_user_url = 'rating/api/user/register/'
user_login_url = 'rating/token-auth'
user_profile_url = 'rating/api/user/'
restaurants_url = 'rating/api/restaurants/'
ratings_url = 'rating/api/ratings/'

user_data = {"username": "test_user", "password": "test_password", "email": "test_user@mail.com",
             "first_name": "test_user_first_name", "last_name": "test_user_last_name"}
updated_user_data = {"first_name": "updated_first_name", "last_name": "updated_last_name"}
user_login_data = {"username": "test_user", "password": "test_password"}
restaurant_data = {"name": "test_restaurant_name", "food_type": "some_type_of_food", "address": "new_way_street_91"}
rating_data = {"restaurant": 1, "rating": 4}
auth_token = ''
user_id = ''
restaurant_id = ''
rating_id = ''


def test_register_user():
    response = requests.post(url=base_url + register_user_url, json=user_data)
    assert str(response) == '<Response [201]>'


def test_login_user():
    response = requests.post(url=base_url + user_login_url, json=user_login_data)
    global auth_token
    auth_token = response.json()["token"]
    assert str(response) == '<Response [200]>'


def test_get_user_profile():
    response = requests.get(url=base_url + user_profile_url, headers={"Authorization": "token " + auth_token})
    global user_id
    user_id = response.json()[0]["id"]
    assert str(response) == '<Response [200]>'
    assert response.json()[0]["username"] == user_data["username"]


def test_update_user_profile():
    update_response = requests.patch(url=base_url + user_profile_url + str(user_id) + "/",
                                     headers={"Authorization": "token " + auth_token}, json=updated_user_data)
    assert str(update_response) == '<Response [200]>'
    get_response = requests.get(url=base_url + user_profile_url, headers={"Authorization": "token " + auth_token})
    assert str(get_response) == '<Response [200]>'
    assert get_response.json()[0]["first_name"] == updated_user_data["first_name"]
    assert get_response.json()[0]["last_name"] == updated_user_data["last_name"]


def test_create_restaurant():
    response = requests.post(url=base_url + restaurants_url, json=restaurant_data,
                             headers={"Authorization": "token " + auth_token})
    global restaurant_id
    restaurant_id = response.json()['id']
    assert str(response) == '<Response [200]>'


def test_get_restaurant():
    response = requests.get(url=base_url + restaurants_url + str(restaurant_id) + "/",
                            headers={"Authorization": "token " + auth_token})
    assert str(response) == '<Response [200]>'
    assert response.json()["name"] == restaurant_data["name"]


def test_update_restaurant():
    response = requests.patch(url=base_url + restaurants_url + str(restaurant_id) + "/",
                              json={"name": "updated_test_restaurant_name"},
                              headers={"Authorization": "token " + auth_token})
    print(response.json())
    assert str(response) == '<Response [200]>'
    get_response = requests.get(url=base_url + restaurants_url + str(restaurant_id) + "/",
                                headers={"Authorization": "token " + auth_token})
    assert str(get_response) == '<Response [200]>'
    assert get_response.json()["name"] == "updated_test_restaurant_name"


def test_create_rating():
    response = requests.post(url=base_url + ratings_url, json=rating_data,
                             headers={"Authorization": "token " + auth_token})
    global rating_id
    rating_id = response.json()['id']
    assert str(response) == '<Response [200]>'


def test_update_rating():
    response = requests.patch(url=base_url + ratings_url + str(rating_id) + "/",
                              json={"rating": 5},
                              headers={"Authorization": "token " + auth_token})
    assert str(response) == '<Response [200]>'
    get_response = requests.get(url=base_url + ratings_url + str(rating_id) + "/",
                                headers={"Authorization": "token " + auth_token})
    assert str(get_response) == '<Response [200]>'
    assert get_response.json()["rating"] == 5


def test_delete_restaurant():
    response = requests.delete(url=base_url + restaurants_url + str(restaurant_id) + "/",
                               headers={"Authorization": "token " + auth_token})
    assert str(response) == '<Response [204]>'
    get_response = requests.get(url=base_url + restaurants_url + str(restaurant_id) + "/",
                                headers={"Authorization": "token " + auth_token})
    assert str(get_response) == '<Response [404]>'
