from rest_framework import serializers
from .models import Users,UserRoles
from django.contrib.auth.hashers import make_password

class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = ['role_id', 'role_name']

class UserSerializer(serializers.ModelSerializer):
    role = UserRolesSerializer(read_only = True)
    class Meta:
        model = Users
        fields = ['user_id', 'username', 'email', 'password_hash', 'role', 'profile_picture', 'bio', 'created_at', 'updated_at']
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password_hash', None)
        if password:
            validated_data['password_hash'] = make_password(password)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.get('password_hash', None)
        if password:
            instance.password_hash = make_password(password)
            validated_data.pop('password_hash')
        return super().update(instance, validated_data)