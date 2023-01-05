from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from users.models import User


def validate_phone_no(phone_no):
    if phone_no not in [None, ''] and User.objects.filter(phone_no=phone_no).exists():
        raise ValidationError(_('%(phone_no)s should be either None or unique'))


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=32, write_only=True, validators=[validate_password])
    phone_no = PhoneNumberField(required=False, default=None, validators=[validate_phone_no])

    class Meta:
        model = User
        exclude = (
            'id',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )
        read_only_fields = (
            'user_id',
            'is_email_verified',
            'is_superuser',
            'is_staff',
            'is_active',
            'joined_on',
        )

    def create(self, validated_data):
        try:
            user = User.objects.create_user(str(validated_data.pop("email")).lower(), validated_data.pop("password"),
                                            validated_data.pop("phone_no"), **validated_data)
            return user
        except IntegrityError as e:
            error = dict({'email': "Another user with this email already exists."})
            raise serializers.ValidationError(error)