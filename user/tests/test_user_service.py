from django.test import TestCase
import rest_framework
from user.models import User
from user.services import post_user_signup_data


class TestRoutineService(TestCase):
    """
    post_user_signup_data 함수를 검증하는 기능 합니다.
    """

    def setUp(self) -> None:
        self.user_data = {
            "email": "test@naver.com",
            "password": "PassW@rd!",
            "nickname": "test",
        }
        self.low_password_user_data = {
            "email": "test@naver.com",
            "password": "Pas",
            "nickname": "test",
        }
        self.not_special_character_data = {
            "email": "test@naver.com",
            "password": "password",
            "nickname": "test",
        }
        self.not_email_data = {
            "email": str,
            "password": "PassW@rd!",
            "nickname": "test",
        }

    def test_post_user_signup_data(self):
        """
        post_user_signup_data service 를 검증 합니다.
        """
        post_user_signup_data(user_data=self.user_data)

        new_user = User.objects.get(email=self.user_data["email"])

        self.assertEqual(new_user.email, self.user_data["email"])
        self.assertEqual(new_user.nickname, self.user_data["nickname"])

    def test_when_not_rules_len_password_post_user_signup_data(self):
        """
        post_user_signup_data service 를 검증 합니다.
        case : 비밀번호 8 글자 이하 일 때
        """

        with self.assertRaises(rest_framework.exceptions.ValidationError):
            post_user_signup_data(user_data=self.low_password_user_data)

    def test_when_not_rules_not_special_character_post_user_signup_data(self):
        """
        post_user_signup_data service 를 검증 합니다.
        case : 특수문자 가 없을 때
        """

        with self.assertRaises(rest_framework.exceptions.ValidationError):
            post_user_signup_data(user_data=self.not_special_character_data)

    def test_when_not_email_post_user_signup_data(self):
        """
        post_user_signup_data service 를 검증 합니다.
        case :  eamil 형식이 아닐 경우
        """

        with self.assertRaises(rest_framework.exceptions.ValidationError):
            post_user_signup_data(user_data=self.not_email_data)
