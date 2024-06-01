from django.db import models
from account.models import CustomUser
import logging
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q


class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')


class UserFriendManager:
    def __init__(self, request):
        self.request = request

    def search_other_user(self):
        resp_dict = {'status': False, 'message': 'Something went wrong. Please try again later.', 'data': {}}
        try:
            queryset = CustomUser.objects.all()
            keyword = self.request.data.get('keyword', None)  # Corrected from self.request.get to self.request.GET.get

            if keyword:
                if '@' in keyword:
                    queryset = queryset.filter(email__iexact=keyword)
                else:
                    queryset = queryset.filter(username__icontains=keyword)
            queryset = queryset.values('username', 'email')
            resp_dict['status'] = True
            resp_dict['message'] = "Got data successfully"
            resp_dict['data']['matched_user'] = list(queryset)
        except Exception as e:
            logging.error('Getting exception on search_other_user', repr(e))

        return resp_dict


    def send_friend_request(self):
        resp_dict = {'status': False, 'message': 'Something went wrong. Please try again later.'}
        from_user = self.request.user
        to_user_id = self.request.data.get('to_user_id')

        errors = None
        if from_user.id == to_user_id:
            errors = "You can't send a friend request to yourself."
        else:
            try:
                to_user = CustomUser.objects.get(id=to_user_id)
            except CustomUser.DoesNotExist:
                errors = 'User does not exist.'

            if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
                errors = 'Friend request already sent.'

            one_minute_ago = timezone.now() - timedelta(minutes=1)
            recent_requests_count = FriendRequest.objects.filter(
                from_user=from_user,
                timestamp__gte=one_minute_ago).count()

            if recent_requests_count >= 3:
                errors = 'You can only send up to 3 friend requests per minute.'

            else:
                FriendRequest.objects.create(from_user=from_user, to_user=to_user)

        if errors:
            resp_dict['message'] = errors

        else:
            resp_dict['status'] = True
            resp_dict['message'] = 'Friend request sent.'

        return resp_dict

    def accept_reject_friend_request(self):
        resp_dict = {'status': False, 'message': 'Something went wrong. Please try again later.'}
        request_id = self.request.data.get('request_id')
        action = self.request.data.get('action')
        error = None


        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=self.request.user, status='pending')
        except FriendRequest.DoesNotExist:
            error = 'Friend request does not exist.'

        if error:
            resp_dict['message'] = error
        else:
            message = None
            if action == 'accept':
                friend_request.status = 'accepted'
                friend_request.save()
                message = 'Friend request accepted'
                resp_dict['status'] = True
            elif action == 'reject':
                friend_request.status = 'rejected'
                friend_request.save()
                message = 'Friend request rejected'
                resp_dict['status'] = True
            else:
                message = 'Invalid action specified'

            resp_dict['message'] = message

        return resp_dict

    def get_all_friend_list(self):
        resp_dict = {'status': False, 'message': 'Something went wrong. Please try again later.', 'data': {}}
        try:
            friends = CustomUser.objects.filter(
                Q(sent_requests__to_user=self.request.user, sent_requests__status='accepted') |
                Q(received_requests__from_user=self.request.user, received_requests__status='accepted')
            ).values('id', 'username', 'email').distinct()

            friend_list = [{'id': friend['id'], 'username': friend['username'], 'email': friend['email']} for friend in friends]

            resp_dict['status'] = True
            resp_dict['message'] = "Got data successfully"
            resp_dict['data']['friend_list'] = friend_list
        except Exception as e:
            logging.error('Getting exception on get_all_friend_list', repr(e))

        return resp_dict

    def get_all_friend_request_list(self):
        resp_dict = {'status': False, 'message': 'Something went wrong. Please try again later.', 'data': {}}
        try:
            friends = CustomUser.objects.filter(sent_requests__to_user=self.request.user, sent_requests__status='pending'
            ).values('id', 'username', 'email')

            received_friend_request_list = [{'id': friend['id'], 'username': friend['username'], 'email': friend['email']} for friend in friends]

            resp_dict['status'] = True
            resp_dict['message'] = "Got data successfully"
            resp_dict['data']['friend_request'] = received_friend_request_list
        except Exception as e:
            logging.error('Getting exception on get_all_friend_request_list, repr(e)')

        return resp_dict