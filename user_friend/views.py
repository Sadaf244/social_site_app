from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from account.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination

class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
class SearchOtherUser(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            user_friend_manager = UserFriendManager(request)
            save_user_resp = user_friend_manager.search_other_user()
            resp_dict['status'] = save_user_resp['status']
            resp_dict['message'] = save_user_resp['message']
            resp_dict['data'] = save_user_resp['data']
        except Exception as e:
            logging.error('Error in getting SearchUserView', repr(e))
        return JsonResponse(resp_dict, status=200)


class SendFriendRequest(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            send_friend_request_manager = UserFriendManager(request)
            save_user_resp = send_friend_request_manager.send_friend_request()
            resp_dict['status'] = save_user_resp['status']
            resp_dict['message'] = save_user_resp['message']
        except Exception as e:
            logging.error('Error in getting SendFriendRequestView', repr(e))
        return JsonResponse(resp_dict, status=200)


class AcceptRejectFriendRequest(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            accept_reject_request_manager = UserFriendManager(request)
            save_user_resp = accept_reject_request_manager.accept_reject_friend_request()
            resp_dict['status'] = save_user_resp['status']
            resp_dict['message'] = save_user_resp['message']
        except Exception as e:
            logging.error('Error in getting AcceptRejectFriendRequestView', repr(e))
        return JsonResponse(resp_dict, status=200)

class GetAllFriendList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            get_all_friend_list_manager = UserFriendManager(request)
            save_user_resp = get_all_friend_list_manager.get_all_friend_list()
            resp_dict['status'] = save_user_resp['status']
            resp_dict['message'] = save_user_resp['message']
            resp_dict['data'] = save_user_resp['data']
        except Exception as e:
            logging.error('Error in getting GetAllFriendList', repr(e))
        return JsonResponse(resp_dict, status=200)


class ReceivedFriendRequestList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            get_all_friend_request_list_manager = UserFriendManager(request)
            save_user_resp = get_all_friend_request_list_manager.get_all_friend_request_list()
            resp_dict['status'] = save_user_resp['status']
            resp_dict['message'] = save_user_resp['message']
            resp_dict['data'] = save_user_resp['data']
        except Exception as e:
            logging.error('Error in getting GetAllFriendList', repr(e))
        return JsonResponse(resp_dict, status=200)