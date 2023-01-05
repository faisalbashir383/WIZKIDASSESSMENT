import uuid
from django.db import models
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, phone_no, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            phone_no=phone_no,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, phone_no, **extra_fields):
        return self._create_user(email, password, False, False, phone_no, **extra_fields)

    def create_superuser(self, email, password, phone_no, **extra_fields):
        return self._create_user(email, password, True, True, phone_no, **extra_fields)


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """

    def to_python(self, value):
        value = super(LowercaseEmailField, self).to_python(value)
        if value:
            return value.lower()
        return value


def set_name(instance, filename):
    """
    """
    ext = filename.split('.')[-1]
    if instance.pk:
        return '{}.{}'.format(instance.user_id, ext)
    else:
        pass
        # do something if pk is not there yet


class User(AbstractBaseUser, PermissionsMixin):
    """
    User Table, which will provide login functionality
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Required:
        email
        password
        first_name
        last_name
        phone_no
    """
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=150, null=True)
    email = LowercaseEmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    user_id = models.UUIDField(default=uuid.uuid4, unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_email_verified = models.BooleanField(_('email verified'), default=False)
    is_phone_no_verified = models.BooleanField(_('Phone no verified'), default=False)
    phone_no = PhoneNumberField(null=True, default=None, blank=True, unique=True)
    reset_token = models.CharField(_('Reset Token'), max_length=5, default=0)
    joined_on = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return str(self.phone_no)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)