from unittest.mock import patch
import pytest
from marshmallow import ValidationError
from appserver.service.users_service import UserService
import appserver.data.user_mapper
import appserver.utils.firebase
from appserver.service.exceptions import NotFoundError, UserExistsError


@patch.object(appserver.data.user_mapper.UserMapper, 'find_one_and_update')
@patch.object(appserver.utils.firebase.Firebase, 'decode_token')
def test_login_if_user_not_found_raises_notfounderror(firebase_mock, um_mock, user_data):
    firebase_mock.return_value = user_data.valid_user
    um_mock.return_value = None
    with pytest.raises(NotFoundError):
        UserService.login(user_data.valid_token)


def test_modify_profile_if_wrong_schema_raises_validationerror():
    pass


@patch.object(appserver.service.users_service.UserService, '_user_exists')
def test_register_if_user_exists_raises_userexistserror(user_exists_mock, user_data):
    user_exists_mock.return_value = True
    with pytest.raises(UserExistsError):
        UserService.register(user_data.valid_user)


def test_register_if_wrong_schema_raises_validationerror(user_data):
    with pytest.raises(ValidationError):
        UserService.register(user_data.invalid_user)


@patch.object(appserver.data.user_mapper.UserMapper, 'get_one')
def test_get_profile_if_not_found_raises_notfounderror(get_one_mock, user_data):
    get_one_mock.return_value = None
    with pytest.raises(NotFoundError):
        UserService.get_profile(user_data.uid)