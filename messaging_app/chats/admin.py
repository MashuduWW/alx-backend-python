from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Conversation, Message

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Conversation)
admin.site.register(Message)
