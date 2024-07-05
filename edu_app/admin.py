from django.contrib import admin
from .models import User, Branch, ClassInfo, ClassSchedule, Request, Subject, Attendance

admin.site.register(User)
admin.site.register(Branch)
admin.site.register(Subject)
admin.site.register(ClassInfo)
admin.site.register(ClassSchedule)
admin.site.register(Request)
admin.site.register(Attendance)