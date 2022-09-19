from rest_framework.test import APIClient, APITestCase
from user.models import User


class TestUserSignUpAPI(APITestCase):
    """
    User의 회원가입 API 를 검증 합니다.
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

    def test_signup(self) -> None:
        """
        UserView 의 회원가입 함수를 검증 합니다.
        """
        client = APIClient()
        url = "/user/signup"
        response = client.post(
            url,
            self.user_data,
        )
        result = response.json()

        self.assertEqual(result["message"], "회원가입을 성공하였습니다")
        self.assertEqual(response.status_code, 200)

    def test_when_not_rules_len_password_sigunup(self) -> None:
        """
        UserView 의 회원가입 함수를 검증 합니다.
        case: 비밀번호 8글자 이하 일 때
        """
        client = APIClient()
        url = "/user/signup"
        response = client.post(
            url,
            self.low_password_user_data,
        )
        result = response.json()

        self.assertEqual(result["message"], "비밀번호는 8자 이상 특수문자 포함해 입력해주세요")
        self.assertEqual(response.status_code, 400)

    def test_when_not_rules_not_special_character_signup(self) -> None:
        """
        UserView 의 회원가입 함수를 검증 합니다.
        case: 특수문자 가 없을 때
        """
        client = APIClient()
        url = "/user/signup"
        response = client.post(
            url,
            self.not_special_character_data,
        )
        result = response.json()

        self.assertEqual(result["message"], "비밀번호는 8자 이상 특수문자 포함해 입력해주세요")
        self.assertEqual(response.status_code, 400)


class LoginTestCase(APITestCase):
    """
    로그인 API 를 검증 합니다.
    """

    def setUp(self) -> None:
        self.user_data = {
            "email": "test@naver.com",
            "password": "PassW@rd!",
            "nickname": "test",
        }
        self.wrong_password_user_data = {
            "email": "test@naver.com",
            "password": "Pa",
            "nickname": "test",
        }
        self.user = User.objects.create(**self.user_data)
        self.user.set_password(self.user_data["password"])
        self.user.save()

    def test_login(self):
        """
        로그인 API 를 검증 합니다.
        """
        url = "/user/login"
        self.user_data.pop("nickname")
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, 200)

    def test_when_wrong_password_login(self):
        """
        로그인 API 를 검증 합니다.
        case : 비밀번호 가 틀릴 경우
        """
        url = "/user/login"
        self.user_data.pop("nickname")
        response = self.client.post(url, self.wrong_password_user_data)
        self.assertEqual(response.status_code, 401)

    def test_when_not_data_login(self):
        """
        로그인 API 를 검증 합니다.
        case : 비밀번호를 입력하지 않았을 경우
        """
        url = "/user/login"
        self.user_data.pop("password")
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, 400)
