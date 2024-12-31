from rest_framework import serializers
from django.contrib.auth.hashers import check_password

from apps.users.models import User

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    name + password or email is needed
    """
    name = serializers.CharField(max_length=100, required=False, allow_null=True)
    email = serializers.EmailField(required=False, allow_null=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if not attrs.get('name') and not attrs.get('email'):
            raise serializers.ValidationError('Either name or email is required.')
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """
    get user info
    """
    class Meta:
        model = User
        fields = ('email', 'name', 'date_joined')


class UpdateUserSerializer(serializers.Serializer):
    """
    patch user info
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        # パスワードをハッシュ化して保存
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
