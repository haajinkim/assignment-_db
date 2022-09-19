from rest_framework.test import APIClient, APITestCase
from user.models import User
from routine.models import Routine, RoutineResult, RoutineDay
from routine.services import routine_post_service


class TestRoutineAPI(APITestCase):
    """
    Routine 의 API를 테스트 합니다.
    """

    def setUp(self) -> None:

        self.user_data = {
            "email": "test@naver.com",
            "password": "PassW@rd!",
            "nickname": "test",
        }

        self.user = User.objects.create(**self.user_data)
        self.user.set_password(self.user_data["password"])
        self.user.save()

        self.request_data = {
            "account_id": self.user.id,
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "days": ["MON", "WED", "SAT"],
            "is_alarm": True,
        }

        self.update_data = {
            "title": "update! title",
            "category": "MIRACLE",
            "goal": "update! goal",
            "days": ["TUS", "TUR", "SAT"],
            "is_alarm": False,
        }

    def test_routine_post(self) -> None:
        """
        Routine 의 post api 를 테스트 합니다.
        """
        client = APIClient()
        client.force_authenticate(user=self.user)

        url = "/routine/"

        response = client.post(url, self.request_data, format="json")
        result = response.json()

        new_routine = Routine.objects.get(account_id_id=self.user.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["data"]["routine_id"], new_routine.id)
        self.assertEqual(
            result["message"]["msg"], "You have successfully created the routine."
        )
        self.assertEqual(result["message"]["status"], "ROUTINE_CREATE_OK")

    def test_when_not_certified_routine_post(self) -> None:
        """
        Routine 의 post api 를 테스트 합니다.
        case : 인증되지 않는 유저 일 때
        """
        client = APIClient()

        url = "/routine/"

        response = client.post(url, self.request_data, format="json")
        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            result["detail"], "Authentication credentials were not provided."
        )

    def test_when_none_user_routine_post(self) -> None:
        """
        Routine 의 post api 를 테스트 합니다.
        case: 없는 유저 ID 로 post를 했을 경우
        """
        client = APIClient()
        client.force_authenticate(user=self.user)

        url = "/routine/"

        self.request_data["account_id"] = 9999

        response = client.post(url, self.request_data, format="json")
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "없는 유저 입니다.")

    def test_routine_to_day_get(self) -> None:
        """
        Rouitne 의 요일별 get api를 테스트 합니다.
        """

        client = APIClient()
        client.force_authenticate(user=self.user)

        target_routine = routine_post_service(request_data=self.request_data)
        tartget_routine_result = RoutineResult.objects.get(routine_id_id=target_routine)

        url = f"/routine/?account_id={self.user.id}&today=2022-09-19"

        response = client.get(
            url,
        )

        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            result["data"][0]["goal"], "Increase your problem-solving skills"
        )
        self.assertEqual(result["data"][0]["title"], "problem solving")
        self.assertEqual(result["data"][0]["result"], tartget_routine_result.result)
        self.assertEqual(result["data"][0]["id"], target_routine)
        self.assertEqual(result["message"]["msg"], "Routine lookup was successful.")
        self.assertEqual(result["message"]["status"], "ROUTINE_LIST_OK")

    def test_when_not_certified_routine_to_day_get(self) -> None:
        """
        Routine 의 get api를 테스트 합니다.
        case : 인증되지 않는 유저 일 때
        """
        client = APIClient()

        url = "/routine/"

        response = client.get(
            url,
        )
        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            result["detail"], "Authentication credentials were not provided."
        )

    def test_when_none_rouitne_routine_to_day_get(self) -> None:
        """
        Rouitne 의 요일별 get api를 테스트 합니다.
        case: 루틴을 조회할 수 없을 때
        """

        client = APIClient()
        client.force_authenticate(user=self.user)

        routine_post_service(request_data=self.request_data)

        url = f"/routine/?account_id={self.user.id}&today=2020-09-20"

        response = client.get(
            url,
        )

        result = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "루틴을 찾을 수 없습니다.")

    def test_routine_short_get(self) -> None:
        """
        Routine 의 단건 get api를 테스트 합니다.
        """

        client = APIClient()
        client.force_authenticate(user=self.user)

        target_routine = routine_post_service(request_data=self.request_data)
        target_routine_result = RoutineResult.objects.get(routine_id_id=target_routine)
        target_routine_days = RoutineDay.objects.get(routine_id_id=target_routine)

        url = f"/routine/?account_id={self.user.id}&routine_id={target_routine}"

        response = client.get(
            url,
        )
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["data"]["goal"], "Increase your problem-solving skills")
        self.assertEqual(result["data"]["title"], "problem solving")
        self.assertEqual(result["data"]["result"], target_routine_result.result)
        self.assertEqual(result["data"]["id"], target_routine)
        self.assertEqual(result["data"]["days"], target_routine_days.day)
        self.assertEqual(result["message"]["msg"], "Routine lookup was successful.")
        self.assertEqual(result["message"]["status"], "ROUTINE_DETAIL_OK")

    def test_when_not_certified_routine_short_get(self) -> None:
        """
        Routine 의 단건 get api를 테스트 합니다.
        case : 인증되지 않는 유저 일 때
        """
        client = APIClient()

        url = "/routine/"

        response = client.get(
            url,
        )
        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            result["detail"], "Authentication credentials were not provided."
        )

    def test_when_none_rouitne_routine_short_get(self) -> None:
        """
        Routine 의 단건 get api를 테스트 합니다.
        case: 루틴을 조회할 수 없을 때
        """

        client = APIClient()
        client.force_authenticate(user=self.user)

        routine_post_service(request_data=self.request_data)

        url = f"/routine/?account_id={self.user.id}&routine_id={999}"

        response = client.get(
            url,
        )

        result = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "루틴을 찾을 수 없습니다.")

    def test_routine_put(self):
        """
        Routine 의 put api를 테스트 합니다.
        """

        client = APIClient()
        client.force_authenticate(user=self.user)

        target_routine = routine_post_service(request_data=self.request_data)

        url = "/routine/"

        self.update_data["routine_id"] = target_routine
        response = client.put(url, self.update_data, format="json")

        result = response.json()

        target_routine_days = RoutineDay.objects.get(routine_id_id=target_routine)
        target_routine_obj = Routine.objects.get(id=target_routine)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["message"]["msg"], "The routine has been modified.")
        self.assertEqual(result["message"]["status"], "ROUTINE_UPDATE_OK")
        self.assertEqual(result["data"]["routine_id"], target_routine)
        self.assertEqual(target_routine_obj.title, "update! title")
        self.assertEqual(target_routine_obj.category, "MIRACLE")
        self.assertEqual(target_routine_obj.goal, "update! goal")
        self.assertEqual(target_routine_obj.is_alarm, False)
        self.assertEqual(target_routine_days.day, "['TUS', 'TUR', 'SAT']")

    def test_when_not_certified_routine_put(self) -> None:
        """
        Routine 의 put api를 테스트 합니다.
        case : 인증되지 않는 유저 일 때
        """
        client = APIClient()

        url = "/routine/"

        response = client.put(
            url,
        )
        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            result["detail"], "Authentication credentials were not provided."
        )

    def test_when_none_routine_put(self):
        """
        Routine 의 put api를 테스트 합니다.
        case: 없는 Routine 을 수정하려고 할 때
        """

        client = APIClient()
        client.force_authenticate(user=self.user)

        routine_post_service(request_data=self.request_data)

        url = "/routine/"

        self.update_data["routine_id"] = 999
        response = client.put(url, self.update_data, format="json")

        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "없는 Routine 입니다.")

    def test_routine_delete(self):
        """
        Routine 의 delete api 를 테스트합니다.
        """

        client = APIClient()
        client.force_authenticate(user=self.user)

        target_routine = routine_post_service(request_data=self.request_data)

        url = "/routine/"

        delete_data = {"routine_id": target_routine, "account_id": self.user.id}

        response = client.delete(url, delete_data, format="json")

        result = response.json()

        target_routine_obj = Routine.objects.get(id=target_routine)
        target_routine_result = RoutineResult.objects.get(routine_id_id=target_routine)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["message"]["msg"], "The routine has been deleted.")
        self.assertEqual(result["message"]["status"], "ROUTINE_DELETE_OK")
        self.assertEqual(result["data"]["routine_id"], target_routine)
        self.assertEqual(target_routine_obj.is_alarm, False)
        self.assertEqual(target_routine_obj.is_deleted, True)
        self.assertEqual(target_routine_result.is_deleted, True)

    def test_when_not_certified_routine_delete(self) -> None:
        """
        Routine 의 delete api를 테스트 합니다.
        case : 인증되지 않는 유저 일 때
        """
        client = APIClient()

        url = "/routine/"

        response = client.delete(
            url,
        )
        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            result["detail"], "Authentication credentials were not provided."
        )

    def test_when_none_routine_delete(self):
        """
        Routine 의 delete api 를 테스트합니다.
        case: 없는 Routine 을 수행하려고 할 때
        """

        client = APIClient()
        client.force_authenticate(user=self.user)

        routine_post_service(request_data=self.request_data)

        url = "/routine/"

        delete_data = {"routine_id": 9999, "account_id": self.user.id}

        response = client.delete(url, delete_data, format="json")

        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "없는 Routine 입니다.")

    def test_routin_result_put(self):
        """
        Routine result 의 결과를 수정하는 put api 를 검증 합니다.
        """
        client = APIClient()
        client.force_authenticate(user=self.user)

        target_routine = routine_post_service(request_data=self.request_data)

        update_data = {"routine_id": target_routine, "result": "TRY"}
        url = "/routine/result"

        response = client.put(url, update_data, format="json")
        result = response.json()

        target_routine_result = RoutineResult.objects.get(routine_id_id=target_routine)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            result["message"]["msg"],
            "You have successfully created the routine result.",
        )
        self.assertEqual(result["message"]["status"], "ROUTINE_RESULT_UPDATE_OK")
        self.assertEqual(result["data"]["routine_id"], target_routine)
        self.assertEqual(target_routine_result.result, "TRY")

    def test_when_not_certified_routine_result_put(self) -> None:
        """
        Routine result 의 결과를 수정하는 put api 를 검증 합니다.
        case : 인증되지 않는 유저 일 때
        """
        client = APIClient()

        url = "/routine/result"

        response = client.put(
            url,
        )
        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            result["detail"], "Authentication credentials were not provided."
        )

    def test_when_none_routine_result_put(self):
        """
        Routine result 의 결과를 수정하는 put api 를 검증 합니다.
        case: 없는 Routine 을 수행하려고 할 때
        """

        client = APIClient()
        client.force_authenticate(user=self.user)

        routine_post_service(request_data=self.request_data)

        update_data = {"routine_id": 9999, "result": "TRY"}

        url = "/routine/result"

        response = client.put(url, update_data, format="json")

        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "없는 Routine 입니다.")
