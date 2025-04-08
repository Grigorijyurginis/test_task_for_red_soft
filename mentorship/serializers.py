from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    mentor_username = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'phone', 'email', 'mentor_username', ]

    def create(self, validated_data):
        mentor_username = validated_data.pop('mentor_username', None)
        mentor = None
        if mentor_username:
            mentor = User.objects.filter(username=mentor_username).first()
            if not mentor:
                raise serializers.ValidationError({"mentor_username": "invalid mentor"})

        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            phone=validated_data.get('phone', ''),
            mentor=mentor
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    mentor_username = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'mentor_username', ]

    @staticmethod
    def get_mentor_username(obj):
        return obj.mentor.username if obj.mentor else None


class UserDetailSerializer(serializers.ModelSerializer):
    mentor_username = serializers.SerializerMethodField()
    mentees = serializers.SerializerMethodField()
    mentor = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'phone', 'email', 'mentor', 'mentor_username', 'mentees', ]
        extra_kwargs = {'password': {'write_only': False}, }

    @staticmethod
    def get_mentor_username(obj):
        if obj.mentor:
            return obj.mentor.username
        return None

    @staticmethod
    def get_mentees(obj):
        if obj.is_mentor:
            return [mentee.username for mentee in obj.mentees.all()]
        return []

    def update(self, instance, validated_data):
        mentor_username = validated_data.pop('mentor') if 'mentor' in validated_data else None
        if mentor_username is not None:
            if mentor_username == '':  # для удаления наставника
                instance.mentor = None
            else:
                try:
                    instance.mentor = User.objects.get(username=mentor_username)
                except User.DoesNotExist:
                    raise serializers.ValidationError({"mentor": "invalid mentor"})

        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user != instance:
            rep.pop('password', None)
        if rep.get('mentor_username') is None:
            rep.pop('mentor_username')
        if not rep.get('mentees'):
            rep.pop('mentees')
        return rep
