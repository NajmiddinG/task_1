from django.contrib import admin
from .models import User, Branch, ClassSchedule, Request

admin.site.register(User)
admin.site.register(Branch)
admin.site.register(ClassSchedule)
admin.site.register(Request)