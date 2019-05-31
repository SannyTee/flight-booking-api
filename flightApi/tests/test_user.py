""" Test for user"""
import mock

from flightApi.tests.base import BaseTestCase


class TestUser(BaseTestCase):
    """ Test for user view function"""
    @mock.patch('flightApi.views.user_auth.upload_image', return_value='a url')
    def test_view_user_auth_create_user(self, upload_image_patched_func):
        """Test the api for creating user"""
        body = {
            "first_name": 'new',
            "last_name": 'user',
            "email": 'new_user@mail.com',
            "password": 'Newuser00@',
            "profile_picture": 'file.jpg',
            "confirm_password": 'Newuser00@'
        }
        response = self.test_client().post('/api/v1/auth/signup/', body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Account successfully created')

    def test_view_user_auth_create_user_fail_with_no_matching_password(self):
        """
        Test the api for creating user with password and confirm_password not matching
        """
        body = {
            "first_name": 'new',
            "last_name": 'user',
            "email": 'new_user@mail.com',
            "password": 'Newuser00',
            "profile_picture": 'file.jpg',
            "confirm_password": 'Newuser0'
        }
        expected_response = {
            'status': "error",
            'error': "password and confirm_password does not match",
            'message': "check the password and confirm_password"
        }
        response = self.test_client().post('/api/v1/auth/signup/', body)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, expected_response)

    def test_view_user_auth_create_user_meet_uppercase_password_requirement(self):
        """
         Test the api for creating user with password and confirm_password not matching
        """
        body = {
            "first_name": 'new',
            "last_name": 'user',
            "email": 'new_user@mail.com',
            "password": 'new_user00',
            "profile_picture": 'file.jpg',
            "confirm_password": 'new_user00'
        }
        response = self.test_client().post('/api/v1/auth/signup/', body)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password must contain at least 1 uppercase letter', response.data['error'])

    def test_view_user_auth_create_user_meet_lowercase_password_requirement(self):
        """
         Test the api for creating user with password and confirm_password not matching
        """
        body = {
            "first_name": 'new',
            "last_name": 'user',
            "email": 'new_user@mail.com',
            "password": 'NEWUSER00',
            "profile_picture": 'file.jpg',
            "confirm_password": 'NEWUSER00'
        }
        response = self.test_client().post('/api/v1/auth/signup/', body)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password must contain at least 1 lowercase letter', response.data['error'])

    def test_view_user_auth_create_user_meet_symbol_password_requirement(self):
        """
         Test the api for creating user with password and confirm_password not matching
        """
        body = {
            "first_name": 'new',
            "last_name": 'user',
            "email": 'new_user@mail.com',
            "password": 'newuser00',
            "profile_picture": 'file.jpg',
            "confirm_password": 'newuser00'
        }
        response = self.test_client().post('/api/v1/auth/signup/', body)
        self.assertEqual(response.status_code, 400)
        self.assertIn('The password must contain at least 1 symbol', response.data['error'])

    def test_view_user_auth_create_user_meet_number_password_requirement(self):
        """
         Test the api for creating user with password and confirm_password not matching
        """
        body = {
            "first_name": 'new',
            "last_name": 'user',
            "email": 'new_user@mail.com',
            "password": 'new_user',
            "profile_picture": 'file.jpg',
            "confirm_password": 'new_user'
        }
        response = self.test_client().post('/api/v1/auth/signup/', body)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password must contain at least 1 digit.', response.data['error'])

    @mock.patch('flightApi.views.user_auth.upload_image', return_value='a url')
    def test_view_user_auth_create_user_fail_with_invalid_email(self, upload_image_patched_func):
        """
         Test the api for creating user with password and confirm_password not matching
        """
        body = {
            "first_name": 'new',
            "last_name": 'user',
            "email": 'new_usermail.com',
            "password": 'New_user00',
            "profile_picture": 'file.jpg',
            "confirm_password": 'New_user00'
        }
        response = self.test_client().post('/api/v1/auth/signup/', body)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Enter a valid email address', str(response.data['error']['email']))