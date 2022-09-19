from rest_framework import serializers
from .models import User


class UserSignupSerializer(serializers.ModelSerializer):
    def validate(self, data):
        condition = all(
            x not in ["!", "@", "#", "$", "%", "^", "&", "*", "_"]
            for x in data["password"]
        )

        if len(data["nickname"]) == 0:
            raise serializers.ValidationError("닉네임을 입력해주세요.")
        elif len(data["password"]) < 8 or condition:
            raise serializers.ValidationError("비밀번호는 8자 이상 특수문자 포함해 입력해주세요")
        return data

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        password = user.password
        user.set_password(password)
        user.save()

        return user

    class Meta:
        model = User
        fields = "__all__"
