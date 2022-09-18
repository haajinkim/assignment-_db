import rest_framework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from . models import (
    Routine, 
    RoutineDay, 
    RoutineResult
    )
from . services import (
    routine_post_service, 
    routine_update_service, 
    routine_delete_service, 
    rotuine_to_day_get_service, 
    routine_short_get_service,
    routine_result_put_service
    )

# Create your views here.
class RoutineApiView(APIView):
    """
    Routine 의 CRUD 를 담당하는 기능
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        routine_get_service 함수를 통해서 routine 을 조회합니다.
        request_body 에 'today' 가 있을경우 요일을 기준으로 다건 조회, 없을 경우 단건을 조회합니다.
        """
        if  'today' in request.data :
            try:
                routines = rotuine_to_day_get_service(request_data=request.data)
                if routines == [] :
                    raise Routine.DoesNotExist
                return Response({
                "data": 
                    routines
                ,
                "message": {
                    "msg": "Routine lookup was successful.",
                    "status" : "ROUTINE_LIST_OK"
                }
                }, status.HTTP_200_OK)
            except Routine.DoesNotExist:
                return Response({"message":"루틴을 찾을 수 없습니다."}, status=400)
        else :
            try:
                routine = routine_short_get_service(request_data=request.data)
                if routine == None :
                    raise Routine.DoesNotExist
                return Response({
                    "data": 
                        routine
                    ,
                    "message": {
                        "msg": "Routine lookup was successful.",
                        "status" : "ROUTINE_DETAIL_OK"
                    }
                    
                    }, status.HTTP_200_OK)
            except Routine.DoesNotExist:
                return Response({"message":"루틴을 찾을 수 없습니다."}, status=400)

    def post(self, request):
        """
        routine_post_service 함수를 통해서 routine 을 create 합니다.
        routine_post_service 함수는 new_routin 의 id값을 리턴합니다
        """
        try:
            new_routine = routine_post_service(request_data= request.data)

            return Response({
                "data": {
                    "routine_id": new_routine
                },
                "message": {
                    "msg": "You have successfully created the routine.",
                    "status" : "ROUTINE_CREATE_OK"
                }
                
                }, status.HTTP_200_OK)

        except rest_framework.exceptions.ValidationError:
            return Response({"message":"없는 유저 입니다."}, status=400)

    def put(self, request):
        """
        routine_update_service 함수를 통해서 routine 을 create 합니다.
        routine_update_service 함수는 update_routin 의 id값을 리턴합니다
        """
        try:
            new_routine = routine_update_service(update_data=request.data, account_id = request.user.id)
            return Response({
                "data": {
                    "routine_id": new_routine
                },
                "message": {
                    "masg": "The routine has been modified.",
                    "status" : "ROUTINE_UPDATE_OK"
                }

                }, status.HTTP_200_OK)
        except Routine.DoesNotExist:
            return Response({"message":"없는 Routine 입니다."}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        routine_update_service 함수를 통해서 routine 을 delete 합니다.
        routine_update_service 함수는 update_routin 의 id값을 리턴합니다
        """
        try:
            delete_routine = routine_delete_service(request_data=request.data, account_id = request.user.id)
            return Response({
                "data": {
                    "routine_id": delete_routine
                },
                "message": {
                    "masg": "The routine has been deleted.",
                    "status" : "ROUTINE_DELETE_OK"
                }

                }, status.HTTP_200_OK)
        except RoutineDay.DoesNotExist:
            return Response({"message":"없는 RoutineDay 입니다."}, status.HTTP_400_BAD_REQUEST)
        except Routine.DoesNotExist:
            return Response({"message":"없는 Routine 입니다."}, status.HTTP_400_BAD_REQUEST)


class RoutineResultApiView(APIView):
    """
    Routine 의 대한 결과를 기록하는 기능
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, reqeust):
        try:
            routine_result = routine_result_put_service(request_data=reqeust.data)

            return Response({
                "data": {
                    "routine_id": routine_result
                },
                "message": {
                    "masg": "You have successfully created the routine result.",
                    "status" : "ROUTINE_RESULT_UPDATE_OK"
                }

                }, status.HTTP_200_OK)
        except RoutineResult.DoesNotExist:
            return Response({"message":"없는 Routine 입니다."}, status.HTTP_400_BAD_REQUEST)
