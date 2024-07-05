from rest_framework import serializers
from .models import User, Branch, ClassInfo, ClassSchedule, Request, Subject, Attendance

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'location', 'description', 'date']
        read_only_fields = ['id', 'date']

class UserSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), write_only=True, source='branch')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_active', 'role', 'branch', 'branch_id', 'password']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
            'branch': {'read_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        if not user.password.startswith('pbkdf2_sha256$'): user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password and not instance.password.startswith('pbkdf2_sha256$'):
            instance.set_password(password)
        instance.save()
        return instance

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']
        read_only_fields = ['id']

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name']

class ClassInfoSerializer(serializers.ModelSerializer):
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), allow_null=True)
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), allow_null=True)
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='teacher'), allow_null=True)
    students = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='student'), many=True)

    class Meta:
        model = ClassInfo
        fields = ['id', 'branch', 'subject', 'teacher', 'students', 'description']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['teacher'] = UserShortSerializer(instance.teacher).data if instance.teacher else None
        representation['students'] = UserShortSerializer(instance.students.all(), many=True).data
        representation['branch'] = BranchSerializer(instance.branch).data if instance.branch else None
        representation['subject'] = SubjectSerializer(instance.subject).data if instance.subject else None
        return representation

    def create(self, validated_data):
        students_data = validated_data.pop('students')
        instance = ClassInfo.objects.create(**validated_data)
        instance.students.set(students_data)
        return instance

class ClassScheduleSerializer(serializers.ModelSerializer):
    class_info = serializers.PrimaryKeyRelatedField(queryset=ClassInfo.objects.all(), allow_null=True)
    class Meta:
        model = ClassSchedule
        fields = ['id', 'class_info', 'start_time', 'duration']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['class_info'] = ClassInfoSerializer(instance.class_info).data
        return representation
    
class RequestSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='student'))

    class Meta:
        model = Request
        fields = ['id', 'student', 'subject', 'message', 'status', 'date']
        read_only_fields = ['date']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request'):
            user_role = self.context['request'].user.role
            if user_role in ['branch_admin', 'superuser']:
                self.fields['status'].read_only = False
            else:
                self.fields['status'].read_only = True

    # def validate_student(self, value):
    #     if self.context['request'].user != value:
    #         raise serializers.ValidationError("You can only create requests for yourself.")
    #     return value


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'class_schedule', 'attended', 'date']