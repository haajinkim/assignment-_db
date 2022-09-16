from django.db import transaction
from . serializers import RoutinSerializer
from . models import Routine,RoutineDay





@transaction.atomic
def routin_post_service(account_id: int, reqeust_data: dict) -> int:
    """
    routin 의 post를 담당하는 service 입니다.
    routin id 값을 return 합니다.
    """
    days = reqeust_data.pop("days")

    routinserialzier = RoutinSerializer(data=reqeust_data)
    routinserialzier.is_valid(raise_exception=True)
    new_routine = routinserialzier.save(account_id_id=account_id)

    RoutineDay.objects.create(
        routine_id_id= new_routine.id,
        day = days
    )

    return new_routine.id
    
@transaction.atomic
def routin_update_service(update_data: dict) ->int:
    """
    routin 의 update를 담당하는 service 입니다.
    routin id 값을 return 합니다.
    """
    days = update_data.pop("days")

    update_routine = Routine.objects.get(id=update_data['account_id'])
    update_worry_board_serializer = RoutinSerializer(update_routine, data=update_data, partial=True)
    update_worry_board_serializer.is_valid(raise_exception=True)
    update_worry_board_serializer.save()

    RoutineDay.objects.update(
        routine_id_id= update_routine.id,
        day = days
    )

    return update_routine.id