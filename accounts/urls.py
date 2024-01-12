from django.urls import path
from .api.views import (RejectFriendRequest, AcceptFriendRequestView,
                       SendFriendRequestView, RemoveFromFriends)
from .views import (
    ProfileDetailView, ProfileUpdateView, FindFriendsView,
    FriendReceivedRequestList, FriendSendedRequestList,
    FriendsListView,) 
    

app_name = "accounts"

urlpatterns = [
    path("profile/<uuid:pk>/", ProfileDetailView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("find_friends/", FindFriendsView.as_view(), name="find_friends"),
    path("send_friend_request/", SendFriendRequestView.as_view(), name="send_friend_request"),
    path("friend_received_requests/", FriendReceivedRequestList.as_view(), name='friend_received_requests'),
    path("friend_sended_requests/", FriendSendedRequestList.as_view(), name='friend_sended_requests'),
    path("accept_friend_request/", AcceptFriendRequestView.as_view(), name="accept_friend_request"),
    path("reject_friend_request/<int:pk>/", RejectFriendRequest.as_view(), name="reject_friend_request"),
    path("friends_list/<uuid:user_pk>/", FriendsListView.as_view(), name="friends_list"),
    path("remove_from_friends/<uuid:pk>/", RemoveFromFriends.as_view(), name="remove_from_friends"),
    
]
