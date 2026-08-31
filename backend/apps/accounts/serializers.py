"""
Guardelio — Accounts Serializers
Handles all input validation and output formatting for the auth module.
"""

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import User, StudentProfile


# ─── Registration ──────────────────────────────────────────────────────────────

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Validates and creates a new student account.
    Enforces password strength, unique email/username, and role assignment.
    """
    password  = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'}, label='Confirm Password')

    class Meta:
        model  = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name':  {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value.lower()

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError('This username is already taken.')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password2': 'Passwords do not match.'})
        # Run Django built-in password validators
        try:
            validate_password(attrs['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data, role=User.Role.STUDENT)
        user.set_password(password)
        user.save()
        return user


# ─── Profile ───────────────────────────────────────────────────────────────────

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = StudentProfile
        fields = ('institution', 'bio', 'avatar_name', 'last_active')
        read_only_fields = ('last_active',)


class UserProfileSerializer(serializers.ModelSerializer):
    """Read-only serializer — returns the authenticated user's full profile."""
    profile    = StudentProfileSerializer(read_only=True)
    full_name  = serializers.CharField(read_only=True)
    role_label = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model  = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'role', 'role_label', 'total_xp',
            'is_active', 'date_joined', 'profile',
        )
        read_only_fields = fields


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Partial update serializer — allows updating name and password.
    Students cannot change their own role or email via this endpoint.
    """
    profile          = StudentProfileSerializer(required=False)
    current_password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    new_password     = serializers.CharField(write_only=True, required=False, min_length=8, style={'input_type': 'password'})

    class Meta:
        model  = User
        fields = ('first_name', 'last_name', 'profile', 'current_password', 'new_password')

    def validate(self, attrs):
        user = self.context['request'].user
        new_pw  = attrs.get('new_password')
        curr_pw = attrs.get('current_password')

        if new_pw and not curr_pw:
            raise serializers.ValidationError({'current_password': 'Current password is required to set a new one.'})
        if curr_pw and not user.check_password(curr_pw):
            raise serializers.ValidationError({'current_password': 'Current password is incorrect.'})
        if new_pw:
            try:
                validate_password(new_pw, user=user)
            except DjangoValidationError as e:
                raise serializers.ValidationError({'new_password': list(e.messages)})
        return attrs

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        validated_data.pop('current_password', None)
        new_password = validated_data.pop('new_password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if new_password:
            instance.set_password(new_password)

        instance.save()

        # Update nested profile if data provided
        if profile_data and hasattr(instance, 'profile'):
            profile_serializer = StudentProfileSerializer(
                instance.profile, data=profile_data, partial=True
            )
            if profile_serializer.is_valid(raise_exception=True):
                profile_serializer.save()

        return instance


# ─── Token ─────────────────────────────────────────────────────────────────────

class LoginResponseSerializer(serializers.Serializer):
    """Shape of the login response data payload (for documentation purposes)."""
    access  = serializers.CharField()
    refresh = serializers.CharField()
    user    = UserProfileSerializer()
