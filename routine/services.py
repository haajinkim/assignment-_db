from django.db import transaction
from django.db.models.query_utils import Q
from . serializers import RoutineSerializer
from . models import Routine,RoutineDay,RoutineResult

from datetime import datetime

def change_to_day_of_the_date(date:str) -> str:
    """
    request body 의 today 를 받아서 ex) '2022-09-17' 의 문자열 형식을
    해당 요일로 리턴해주는 함수 입니다. 
    """
    datetime_date = datetime.strptime(date,'%Y-%m-%d')
    date_dict = {0:'MON',1:'TUE',2:'WED',3:'TUR',4:'FRI',5:'SAT',6:'SUN'}
    today = date_dict[datetime_date.weekday()]
    return today


def rotuine_to_day_get_service(request_data: dict) -> dict:
    """
    routine 의 요일별로 get 을 담당하는 service 입니다.
    routinserialzier 의 값을 리턴합니다.
    """

    request_data["today"] = change_to_day_of_the_date(date=request_data["today"])

    cur_routines = Routine.objects.prefetch_related('routineresult_set').prefetch_related('routineday_set').filter(Q(account_id_id=request_data["account_id"])&Q(routineday__day__contains=request_data["today"]))
    routines = RoutineSerializer(cur_routines, many=True).data

    return routines

def routine_short_get_service(request_data: dict) -> dict:
    """
    routine 의 단건 rouitne  get 을 담당하는 service 입니다.
    routinserialzier 의 값을 리턴합니다.
    'days' 를 data 에 포함하기위해 serialzier 후 따로 딕셔너리 문법으로 데이터를 추가합니다.
    """

    cur_routine = Routine.objects.prefetch_related("routineday_set").get(id=request_data["routine_id"])
    if cur_routine.account_id.id == request_data['account_id']:

        rounine = RoutineSerializer(cur_routine).data
        rounine['days'] = cur_routine.routineday_set.get().day

        return rounine

@transaction.atomic
def routine_post_service(request_data: dict) -> int:
    """
    routine 의 post를 담당하는 service 입니다.
    routine id 값을 return 합니다.
    """
    days = request_data.pop("days")

    routineserializer = RoutineSerializer(data=request_data)
    routineserializer.is_valid(raise_exception=True)
    new_routine = routineserializer.save()

    RoutineDay.objects.create(
        routine_id_id= new_routine.id,
        day = days
    )
    RoutineResult.objects.create(
        routine_id_id= new_routine.id
    )

    return new_routine.id
    
@transaction.atomic
def routine_update_service(update_data: dict, account_id:int) ->int:
    """
    routine 의 update를 담당하는 service 입니다.
    routine id 값을 return 합니다.
    """
    days = update_data.pop("days")

    update_routine = Routine.objects.get(id=update_data['routine_id'])
    update_routine_day= RoutineDay.objects.filter(routine_id_id=update_routine)

    if update_routine.account_id.id == account_id:

        update_routinserialzier = RoutineSerializer(update_routine, data=update_data, partial=True)
        update_routinserialzier.is_valid(raise_exception=True)
        update_routinserialzier.save()

        update_routine_day.update(
            day = days
        )


        return update_routine.id

@transaction.atomic
def routine_delete_service(request_data: dict) -> int:
    """
    routine 의 delete를 담당하는 service 입니다.
    삭제 요청시, RoutineDay 모델만 삭제하고
    Routine, RoutineResult 의 is_deleted 를 True 로 수정합니다.
    routine id 값을 return 합니다.
    """

    delete_routine = Routine.objects.get(id=request_data['routine_id'])
    delete_routine_result = RoutineResult.objects.get(routine_id_id=request_data['routine_id'])


    if delete_routine.account_id.id == request_data['account_id']:

        delete_routine_day = RoutineDay.objects.get(routine_id = delete_routine)
        delete_routine_day.delete()

        delete_routine.is_deleted = True
        delete_routine.is_alarm= False
        delete_routine.save()

        delete_routine_result.is_deleted = True
        delete_routine_result.save()

        return delete_routine.id

def routine_result_put_service(request_data:dict) -> int:
    """
    routine_result 의 결과를 수정하는 service입니다.
    routine_id 값을 리턴합니다.
    """

    routine_result = RoutineResult.objects.filter(routine_id_id=request_data['routine_id'])
    if routine_result.get():
        routine_result.update(
            result =  request_data['result']
        )

        return request_data['routine_id']