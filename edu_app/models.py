from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superuser', 'Superuser'),
        ('branch_admin', 'Branch Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    groups = models.ManyToManyField(
        Group,
        related_name='edu_app_user_groups',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='edu_app_user_permissions',
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

class Subject(models.Model):
    name = models.CharField(max_length=255)

class ClassSchedule(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(User, related_name='class_schedules', limit_choices_to={'role': 'student'})
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Request(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    date = models.DateTimeField(auto_now_add=True)
