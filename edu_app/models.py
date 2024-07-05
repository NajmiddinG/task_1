from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class RoleOptions(models.TextChoices):
    SUPERUSER = 'superuser', 'Superuser'
    BRANCH_ADMIN = 'branch_admin', 'Branch Admin',
    TEACHER = 'teacher', 'Teacher',
    STUDENT = 'student', 'Student',

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, first_name=None, last_name=None, role=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        if not user.password.startswith('pbkdf2_sha256$'):
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, first_name=None, last_name=None):
        user = self.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=RoleOptions.SUPERUSER,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=RoleOptions.choices,
                            blank=True, null=True, default=RoleOptions.STUDENT)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    def save(self, *args, **kwargs):
        if self.role == RoleOptions.SUPERUSER:
            self.is_superuser = True
        elif self.role == RoleOptions.BRANCH_ADMIN:
            self.is_superuser = False
        elif self.role == RoleOptions.TEACHER:
            self.is_superuser = False
        elif self.role == RoleOptions.STUDENT:
            self.is_superuser = False
        if self.pk is not None:
            orig = User.objects.get(pk=self.pk)
            if not self.password.startswith('pbkdf2_sha256$') and orig.password != self.password:
                self.set_password(self.password)
        elif not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
            
        super(User, self).save(*args, **kwargs)

class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ClassInfo(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(User, related_name='class_info', limit_choices_to={'role': 'student'})
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return str(self.id)

class ClassSchedule(models.Model):
    class_info = models.ForeignKey(ClassInfo, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    duration = models.TimeField()

    def __str__(self):
        return str(self.id)

class Request(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    status = models.CharField(max_length=20, default='Pending')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE)
    attended = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.class_schedule} - {self.date}"
