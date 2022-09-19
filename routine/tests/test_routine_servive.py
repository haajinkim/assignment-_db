from django.test import TestCase
from user.models import User
import rest_framework
from routine.models import Routine, RoutineDay, RoutineResult
from routine.services import (
    routine_post_service,
    rotuine_to_day_get_service,
    routine_short_get_service,
    routine_update_service,
    routine_delete_service,
    routine_result_put_service,
)


class TestRoutineService(TestCase):
    """
    routine service 함수를 검증하는 test
    """

    def setUp(self) -> None:

        self.user = User.objects.create(email="test@naver.com", nickname="test1")

        self.request_data = {
            "account_id": self.user.id,
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "days": ["MON", "WED", "SAT"],
            "is_alarm": True,
        }

        self.raise_error_not_user_data = {
            "account_id": 999,
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "days": ["MON", "WED", "SAT"],
            "is_alarm": True,
        }

        self.raise_error_not_data = {
            "account_id": 999,
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
        }

        self.update_data = {
            "title": "update_routine",
            "category": "MIRACLE",
            "goal": "fully understand",
            "days": ["TUS", "TUR", "SUN"],
            "is_alarm": False,
        }

    def test_routine_post_service(self) -> None:
        """
        routine_post_service 를 검증 합니다.
        """
        routine_post_service(request_data=self.request_data)

        new_routine = Routine.objects.get(account_id_id=self.user.id)
        new_routine_day = RoutineDay.objects.get(routine_id=new_routine)

        self.assertEqual(self.user.id, new_routine.id)
        self.assertEqual(self.request_data["title"], new_routine.title)
        self.assertEqual(self.request_data["category"], new_routine.category)
        self.assertEqual(self.request_data["goal"], new_routine.goal)
        self.assertEqual(str(["MON", "WED", "SAT"]), new_routine_day.day)
        self.assertEqual(self.request_data["is_alarm"], new_routine.is_alarm)

    def test_when_not_user_routine_post_service(self) -> None:
        """
        routine_post_service 를 검증 합니다.
        case: user 가 없을 때
        """

        with self.assertRaises(rest_framework.exceptions.ValidationError):
            routine_post_service(request_data=self.raise_error_not_user_data)

    def test_when_not_data_routine_post_service(self) -> None:
        """
        routine_post_service 를 검증 합니다.
        case: validation 을 통과 못 했을때
        """

        with self.assertRaises(KeyError):
            routine_post_service(request_data=self.raise_error_not_data)

    def test_rotuine_to_day_get_service(self) -> None:
        """
        routine 의 요일별로 get하는 service 를 검증 합니다.
        """

        request_data = {"account_id": self.user.id, "today": "2022-09-17"}

        routine_post_service(request_data=self.request_data)

        response = rotuine_to_day_get_service(
            account_id=request_data["account_id"], today=request_data["today"]
        )

        self.assertEqual(response[0]["goal"], "Increase your problem-solving skills")
        self.assertEqual(response[0]["id"], 1)
        self.assertEqual(response[0]["result"], "NOT")
        self.assertEqual(response[0]["title"], "problem solving")

    def test_when_wrongdata_rotuine_to_day_get_service(self) -> None:
        """
        routine 의 요일별로 get하는 service 를 검증 합니다.
        case: 잘못된 type 의 데이터가 들어올 경우
        """
        request_data = {"account_id": str, "today": "2022-09-18"}

        with self.assertRaises(TypeError):
            rotuine_to_day_get_service(request_data=request_data)

    def test_routine_short_get_service(self) -> None:
        """
        routine 의 단건 rouitne  get 하는 service 를 검증 합니다.
        """

        new_routine = routine_post_service(request_data=self.request_data)

        request_data = {"routine_id": new_routine, "account_id": self.user.id}

        response = routine_short_get_service(
            routine_id=request_data["routine_id"], account_id=request_data["account_id"]
        )

        self.assertEqual(response["goal"], "Increase your problem-solving skills")
        self.assertEqual(response["id"], 1)
        self.assertEqual(response["result"], "NOT")
        self.assertEqual(response["title"], "problem solving")
        self.assertEqual(response["days"], "['MON', 'WED', 'SAT']")

    def test_when_wrongdata_routine_short_get_service(self) -> None:
        """
        routine 의 단건 rouitne  get 하는 service 를 검증 합니다.
        case: 잘못된 type 의 데이터가 들어올 경우
        """
        request_data = {"routine_id": str, "account_id": self.user.id}

        with self.assertRaises(TypeError):
            routine_short_get_service(request_data=request_data)

    def test_routine_update_service(self) -> None:
        """
        routine 의 update를 담당하는 service 를 검증 합니다.
        """

        new_routine = routine_post_service(request_data=self.request_data)

        self.update_data["routine_id"] = new_routine

        update = routine_update_service(
            update_data=self.update_data, account_id=self.user.id
        )

        update_routine = Routine.objects.get(id=update)
        update_routine_days = RoutineDay.objects.get(routine_id_id=update)

        self.assertEqual(update_routine.title, "update_routine")
        self.assertEqual(update_routine.category, "MIRACLE")
        self.assertEqual(update_routine.goal, "fully understand")
        self.assertEqual(update_routine_days.day, "['TUS', 'TUR', 'SUN']")
        self.assertEqual(update_routine.is_alarm, False)

    def test_when_wrongdata_routine_update_service(self) -> None:
        """
        routine 의 update를 담당하는 service 를 검증 합니다.
        case: validation 을 통과 못햇을 때
        """
        new_routine = routine_post_service(request_data=self.request_data)

        update_data = {
            "title": 1234,
            "category": "MIRACLE",
            "goal": True,
            "days": ["TUS", "TUR", "SUN"],
            "is_alarm": False,
        }
        update_data["routine_id"] = new_routine

        with self.assertRaises(rest_framework.exceptions.ValidationError):
            routine_update_service(update_data=update_data, account_id=self.user.id)

    def test_when_keyerror_routine_update_service(self) -> None:
        """
        routine 의 update를 담당하는 service 를 검증 합니다.
        case:  routine_id가 없을 때
        """
        routine_post_service(request_data=self.request_data)

        with self.assertRaises(KeyError):
            routine_update_service(
                update_data=self.update_data, account_id=self.user.id
            )

    def test_routine_delete_service(self) -> None:
        """
        routine_delete_service 의 delete를 담당하는 service 를 검증 합니다.
        """

        target_routine_id = routine_post_service(request_data=self.request_data)

        delete_data = {"routine_id": target_routine_id, "account_id": self.user.id}

        routine_delete_service(request_data=delete_data)

        target_routine = Routine.objects.get(id=target_routine_id)
        target_routine_result = RoutineResult.objects.get(routine_id_id=target_routine)

        self.assertEqual(target_routine.is_deleted, True)
        self.assertEqual(target_routine.is_alarm, False)
        self.assertEqual(target_routine_result.is_deleted, True)

    def test_when_does_not_exist_test_routine_delete_service(self) -> None:
        """
        routine_delete_service 의 delete를 담당하는 service 를 검증 합니다.
        case: rotuine 아이디가 존재하지 않을 때
        """

        routine_post_service(request_data=self.request_data)

        delete_data = {"routine_id": 999, "account_id": self.user.id}

        with self.assertRaises(Routine.DoesNotExist):
            routine_delete_service(request_data=delete_data)

    def test_when_wrong_data_exist_test_routine_delete_service(self) -> None:
        """
        routine_delete_service 의 delete를 담당하는 service 를 검증 합니다.
        case: 잘못된 데이터 형식이 들어올 때
        """

        routine_post_service(request_data=self.request_data)

        delete_data = {"routine_id": str, "account_id": self.user.id}

        with self.assertRaises(TypeError):
            routine_delete_service(request_data=delete_data)

    def test_routine_result_put_service(self) -> None:
        """
        routine_result 의 결과를 수정하는 service를 검증 합니다.
        """

        new_routine = routine_post_service(request_data=self.request_data)

        request_data = {"routine_id": new_routine, "result": "TRY"}
        routine_result_put_service(request_data=request_data)
        target_routine_result = RoutineResult.objects.get(routine_id_id=new_routine)

        self.assertEqual(target_routine_result.result, "TRY")
        self.assertEqual(new_routine, target_routine_result.routine_id.id)

    def test_when_does_not_exist_routine_result_put_service(self) -> None:
        """
        routine_result 의 결과를 수정하는 service를 검증 합니다.
        case: 없는 routine 을 수정하려고 할 때
        """

        routine_post_service(request_data=self.request_data)

        request_data = {"routine_id": 999, "result": "TRY"}

        with self.assertRaises(RoutineResult.DoesNotExist):
            routine_result_put_service(request_data=request_data)

    def test_when_wrong_data_routine_result_put_service(self) -> None:
        """
        routine_result 의 결과를 수정하는 service를 검증 합니다.
        case: 잘못된 데이터 형식이 들어올 때
        """

        routine_post_service(request_data=self.request_data)

        request_data = {"routine_id": str, "result": "TRY"}

        with self.assertRaises(TypeError):
            routine_result_put_service(request_data=request_data)
