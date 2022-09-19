from rest_framework import exceptions, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from user.services import post_user_signup_data

# Create your views here.


class UserView(APIView):
    """
    회원가입 을 담당하는 기능
    """

    def post(self, request: Request) -> Response:
        """
        post_user_signup_data 함수를 통해서 회원가입을 진행합니다.
        validation 에 통과하지 못할 경우 validation 에러를 리턴 합니다.
        """
        try:
            post_user_signup_data(request.data)
            return Response({"message": "회원가입을 성공하였습니다"}, status=status.HTTP_200_OK)
        except exceptions.ValidationError as e:
            error = "\n".join(
                [str(value) for values in e.detail.values() for value in values]
            )
            return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)
