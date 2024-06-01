from django.contrib import admin
from .models import *
# Register your models here.
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user','to_user', 'status')

admin.site.register(FriendRequest, FriendRequestAdmin)

