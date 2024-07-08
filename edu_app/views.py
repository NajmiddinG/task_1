from rest_framework import viewsets, status, permissions
from .models import User, Branch, ClassInfo, ClassSchedule, Request, Subject, Attendance
from .serializers import (
    UserSerializer, BranchSerializer, SubjectSerializer, ClassInfoSerializer, 
    ClassScheduleSerializer, RequestSerializer, AttendanceSerializer)
from .role_permissions import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"detail": "Successfully logged in"}, status=status.HTTP_200_OK)
    return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_list(request):
    role = request.user.role
    if request.method == 'GET':
        if role == 'superuser':
            users = User.objects.all()
        elif role == 'branch_admin':
            users = User.objects.filter(branch=request.user.branch)
        elif role == 'teacher':
            class_info = ClassInfo.objects.filter(teacher=request.user)
            student_ids = class_info.values_list('students', flat=True)
            users = User.objects.filter(id__in=student_ids)
        elif role == 'student':
            users = User.objects.filter(username=request.user.username)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if role != 'superuser' and role != 'branch_admin':
            return Response(status=status.HTTP_403_FORBIDDEN)

        if role == 'branch_admin':
            if request.data['role'] not in ['teacher', 'student'] or request.data['branch'] != request.user.branch.id: return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    role = request.user.role
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if role == 'branch_admin' and user.branch != request.user.branch or \
        role not in ['superuser', 'branch_admin', 'teacher', 'student'] or \
            (role in ['teacher', 'student'] and user!=request.user):
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def branch_list(request):
    role = request.user.role
    if request.method == 'GET':
        if role == 'superuser':
            branches = Branch.objects.all()
        elif role == 'branch_admin':
            branches = Branch.objects.filter(id=request.user.branch.id)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if role != 'superuser':
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def branch_detail(request, pk):
    role = request.user.role
    try:
        branch = Branch.objects.get(pk=pk)
    except Branch.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if role != 'superuser' and (role != 'branch_admin' or branch != request.user.branch):
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = BranchSerializer(branch)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BranchSerializer(branch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        branch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsSuperuser])
def subject_list(request):
    role = request.user.role
    if request.method == 'GET':
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsSuperuser])
def subject_detail(request, pk):
    role = request.user.role
    try:
        subject = Subject.objects.get(pk=pk)
    except Subject.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def class_info_list(request):
    role = request.user.role
    if request.method == 'GET':
        if role == 'superuser':
            schedules = ClassInfo.objects.all()
        elif role == 'branch_admin':
            schedules = ClassInfo.objects.filter(branch=request.user.branch)
        elif role == 'teacher':
            schedules = ClassInfo.objects.filter(teacher=request.user)
        elif role == 'student':
            schedules = ClassInfo.objects.filter(students=request.user)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ClassInfoSerializer(schedules, many=True)
        
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if role not in ['superuser', 'branch_admin'] or role == 'branch_admin' and request.user.branch.id != request.data['branch']:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ClassInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def class_info_detail(request, pk):
    role = request.user.role
    try:
        schedule = ClassInfo.objects.get(pk=pk)
    except ClassInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if role == 'branch_admin' and schedule.branch != request.user.branch:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        if (role == 'student' and request.user not in schedule.students.all()) or \
        (role == 'teacher' and request.user!=schedule.teacher):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ClassInfoSerializer(schedule)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if role not in ['superuser', 'branch_admin']:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = ClassInfoSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if role not in ['superuser', 'branch_admin']:
            return Response(status=status.HTTP_403_FORBIDDEN)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def class_schedule_list(request):
    role = request.user.role
    if request.method == 'GET':
        if role == 'superuser':
            schedules = ClassSchedule.objects.all()
        elif role == 'branch_admin':
            schedules = ClassSchedule.objects.filter(class_info__branch=request.user.branch)
        elif role == 'teacher':
            schedules = ClassSchedule.objects.filter(class_info__teacher=request.user)
        elif role == 'student':
            schedules = ClassSchedule.objects.filter(class_info__students=request.user)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ClassScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if role not in ['superuser', 'branch_admin']:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ClassScheduleSerializer(data=request.data)
        if serializer.is_valid():
            class_info = serializer.validated_data['class_info']
            if role == 'branch_admin' and class_info.branch != request.user.branch:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def class_schedule_detail(request, pk):
    role = request.user.role
    try:
        schedule = ClassSchedule.objects.get(pk=pk)
    except ClassSchedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if role == 'branch_admin' and schedule.class_info.branch != request.user.branch:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if (role == 'student' and request.user not in schedule.class_info.students.all()) or \
        (role == 'teacher' and request.user!=schedule.class_info.teacher):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ClassScheduleSerializer(schedule)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if role not in ['superuser', 'branch_admin']:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ClassScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            class_info = serializer.validated_data['class_info']
            if role == 'branch_admin' and class_info.branch != request.user.branch:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if role not in ['superuser', 'branch_admin']:
            return Response(status=status.HTTP_403_FORBIDDEN)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def request_list(request):
    role = request.user.role
    
    if request.method == 'GET':
        if role == 'superuser':
            user_requests = Request.objects.all()
        elif role == 'branch_admin':
            user_requests = Request.objects.filter(student__branch=request.user.branch)
        elif role == 'teacher':
            class_info = ClassInfo.objects.filter(teacher=request.user)
            student_ids = class_info.values_list('students', flat=True)
            user_requests = Request.objects.filter(student_id__in=student_ids)
        elif role == 'student':
            user_requests = Request.objects.filter(student=request.user)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = RequestSerializer(user_requests, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        if role != 'student':
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = RequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(student=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def request_detail(request, pk):
    role = request.user.role
    try:
        request_instance = Request.objects.get(pk=pk)
    except Request.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if role == 'superuser':
        pass
    elif role == 'branch_admin':
        if request_instance.student.branch != request.user.branch:
            return Response(status=status.HTTP_403_FORBIDDEN)
    elif role == 'teacher':
        if not ClassInfo.objects.filter(teacher=request.user, students=request_instance.student).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
    elif role == 'student':
        if request_instance.student != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        serializer = RequestSerializer(request_instance, context={'request': request})
        return Response(serializer.data)
    else:
        if role not in ['superuser', 'branch_admin', 'student'] or (request_instance.student != request.user and role == 'student'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        if request.method == 'PUT':
            serializer = RequestSerializer(request_instance, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            request_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def take_attendance(request, class_schedule_id):
    role = request.user.role

    if role not in ['superuser', 'branch_admin', 'teacher']:
        return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        class_schedule = ClassSchedule.objects.get(pk=class_schedule_id)
    except ClassSchedule.DoesNotExist:
        return Response({'error': 'Class schedule not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        attendances = Attendance.objects.filter(class_schedule_id=class_schedule_id)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        data = request.data['attendance']
        serializer = AttendanceSerializer(data=data, many=True, context={'class_schedule': class_schedule})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
