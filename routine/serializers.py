from rest_framework import serializers
from .models import Routine

class RoutineSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    def get_result(self,obj):

        return obj.routineresult_set.get(routine_id=obj).result

    def create(self, validated_data):
        new_routine = Routine.objects.create(**validated_data)
        new_routine.save()            
        return new_routine

    class Meta:
        model = Routine
        fields = ["goal","id","result","title","category","is_alarm","account_id"]
    
        extra_kwargs = {
            "category": {"write_only": True},
            "is_alarm": {"write_only": True},
            "account_id": {"write_only": True},
        }


