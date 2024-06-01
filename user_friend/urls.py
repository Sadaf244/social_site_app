from django.urls import path
from . import views

urlpatterns = [
    path('search-other-user/', views.SearchOtherUser.as_view()),
    path('send-friend-request/', views.SendFriendRequest.as_view()),
    path('accept-reject-friend-request/', views.AcceptRejectFriendRequest.as_view()),
    path('get-all-friend-list/', views.GetAllFriendList.as_view()),
    path('get-all-friend-request-list/', views.ReceivedFriendRequestList.as_view()),
    ]