from rest_framework import serializers
from .models import Routine


class RoutineSerializer(serializers.ModelSerializer):
    """
    Routine Serializer 입니다.
    """
    result = serializers.SerializerMethodField()

    def get_result(self, obj: object) -> object:
        """
        result 를 같이 리턴해주기 위해 SerializerMethodField 이용해 
        역참조 모델을 조회후 result 값을 리턴합니다. 
        """
        return obj.routineresult_set.get(routine_id=obj).result

    def create(self, validated_data: dict) -> object:
        new_routine = Routine.objects.create(**validated_data)
        new_routine.save()
        return new_routine

    class Meta:
        """
        model 과 fields 를 정의합니다.
        extra_kwargs 를 통해 리턴시 리턴하지 않을 값을 설정 하였습니다.
        """
        model = Routine
        fields = ["goal", "id", "result", "title", "category", "is_alarm", "account_id"]

        extra_kwargs = {
            "category": {"write_only": True},
            "is_alarm": {"write_only": True},
            "account_id": {"write_only": True},
        }
