from rest_framework import serializers
from .models import User


class UserSignupSerializer(serializers.ModelSerializer):
    """
    User 의 회원가입 을 위한 Serializer 입니다.
    """
    def validate(self, data):
        """
        validate 함수를 통해 특수문자, 비밀번호 형식을 검증합니다.
        """
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
        """
        create 함수를 통해 obj 를 저장하고, 
        set_password 를 통해 password 를 해싱합니다.
        """
        user = super().create(*args, **kwargs)
        password = user.password
        user.set_password(password)
        user.save()

        return user

    class Meta:
        model = User
        fields = "__all__"
