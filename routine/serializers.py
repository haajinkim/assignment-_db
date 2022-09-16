from rest_framework import serializers
from .models import Routine

class RoutinSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
            new_routine = Routine.objects.create(**validated_data)
            new_routine.save()            
            return new_routine

    class Meta:
        model = Routine
        fields = ["title","category","goal","is_alarm"]
    

