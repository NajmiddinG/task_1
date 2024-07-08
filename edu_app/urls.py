from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    user_list, user_detail, branch_list, branch_detail, 
    subject_list, subject_detail, class_info_list, class_info_detail,
    class_schedule_list, class_schedule_detail, request_list, request_detail,
    take_attendance, login_view, logout_view
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),

    path('branches/', branch_list, name='branch-list'),
    path('branches/<int:pk>/', branch_detail, name='branch-detail'),

    path('subjects/', subject_list, name='subject-list'),
    path('subjects/<int:pk>/', subject_detail, name='subject-detail'),

    path('classes/', class_info_list, name='class_info-list'),
    path('classes/<int:pk>/', class_info_detail, name='class_info-detail'),

    path('class-schedules/', class_schedule_list, name='class-schedule-list'),
    path('class-schedules/<int:pk>/', class_schedule_detail, name='class-schedule-detail'),

    path('requests/', request_list, name='request-list'),
    path('requests/<int:pk>/', request_detail, name='request-detail'),

    path('class-schedule/<int:class_schedule_id>/attendance/take/', take_attendance, name='take_attendance'),
]
