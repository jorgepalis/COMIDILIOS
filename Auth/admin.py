from django.contrib import admin
from .models import User, Message

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'username',
        'is_admin',
        'is_rider',
        'is_vendor',
        'is_client'
    ]
    list_filter = ['is_client', 'is_vendor', 'is_rider']
    search_fields = ['username']

class MsgAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'room',
        'sender',
        'message',
        'created_at',
        'updated_at'
    ]
    list_filter = ['created_at', 'updated_at']
    search_fields = ['sender']


admin.site.register(User, UserAdmin)
admin.site.register(Message, MsgAdmin)
