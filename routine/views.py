import django
from rest_framework.views import APIView
from rest_framework import exceptions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from . models import Routine
from . services import routin_post_service, routin_update_service

# Create your views here.
class RoutineApiView(APIView):
    """
    Routine 의 CRUD 를 담당하는 기능
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        """
        routin_post_service 함수를 통해서 routine 을 create 합니다.
        routin_post_service는 new_routin 의 id값을 리턴합니다
        """
        try:
            new_routine = routin_post_service(account_id=request.user.id, reqeust_data= request.data)
            return Response({
                "data": {
                    "routine_id": new_routine
                },
                "message": {
                    "masg": "You have successfully created the routine.",
                    "status" : "ROUTINE_CREATE_OK"
                }
                
                }, status=200)
        except django.db.utils.IntegrityError:
            return Response({"message":"없는 유저 입니다."}, status=400)

    def put(self, request):
        """
        routin_update_service 함수를 통해서 routine 을 create 합니다.
        routin_update_service update_routin 의 id값을 리턴합니다
        """
        try:
            new_routine = routin_update_service(update_data=request.data)
            return Response({
                "data": {
                    "routine_id": new_routine
                },
                "message": {
                    "masg": "The routine has been modified.",
                    "status" : "ROUTINE_UPDATE_OK"
                }

                }, status=200)
        except Routine.DoesNotExist:
            return Response({"message":"없는 Routine 입니다."}, status=400)