from rest_framework import exceptions, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from user.service import post_user_signup_data
# Create your views here.
class UserView(APIView):
    """
    회원정보 조회 및 회원가입
    """
    def post(self, request: Request) -> Response:
    
        try:
            post_user_signup_data(request.data)
            return Response({"detail": "회원가입을 성공하였습니다"}, status=status.HTTP_200_OK)
        except exceptions.ValidationError as e:
            error = "\n".join([str(value) for values in e.detail.values() for value in values])
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
