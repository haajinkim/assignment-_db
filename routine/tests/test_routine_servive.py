from django.test import TestCase
from user.models import User
import rest_framework
from routine.models import Routine, RoutineDay
from routine.services import routine_post_service

class TestRoutineService(TestCase):
    """
    routine service 함수를 검증하는 test
    """
    def setUp(self) -> None:

        self.user = User.objects.create(email="test@naver.com", nickname="test1")

        self.request_data = {
            "account_id" : self.user.id,
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal" : "Increase your problem-solving skills",
            "days" : ["MON","WED","SAT"],
            "is_alarm" : True
        }

        self.raise_error_not_user_data = {
            "account_id" : 999,
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal" : "Increase your problem-solving skills",
            "days" : ["MON","WED","SAT"],
            "is_alarm" : True
        }

        self.raise_error_not_data = {
            "account_id" : 999,
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal" : "Increase your problem-solving skills",
            "is_alarm" : True
        }


    def test_routine_post_service(self):
        """
        routine_post_service 를 검증 
        """
        routine_post_service(request_data=self.request_data)

        new_routine = Routine.objects.get(account_id_id=self.user.id)
        new_routine_day = RoutineDay.objects.get(routine_id = new_routine)


        self.assertEqual(self.user.id, new_routine.id)
        self.assertEqual(self.request_data['title'], new_routine.title)
        self.assertEqual(self.request_data['category'], new_routine.category)
        self.assertEqual(self.request_data['goal'], new_routine.goal)
        self.assertEqual(str(["MON","WED","SAT"]), new_routine_day.day)
        self.assertEqual(self.request_data['is_alarm'], new_routine.is_alarm)

    def test_when_not_user_routine_post_service(self):
        """
        routine_post_service 를 검증
        case: user 가 없을 때
        """

        with self.assertRaises(rest_framework.exceptions.ValidationError):
            routine_post_service(request_data=self.raise_error_not_user_data)

    def test_when_not_data_routine_post_service(self):
        """
        routine_post_service 를 검증
        case: validation 을 통과 못 했을때
        """

        with self.assertRaises(KeyError):
            routine_post_service(request_data=self.raise_error_not_data)