from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)


class PicManager(models.Manager):
    def create_pic(self, path, des, create_time,like=0):
        pic = self.model(
            path=path,
            description=des,
            createTime=create_time,
            like=like
        )
        pic.save()
        return pic


class Picture(models.Model):

    path = models.TextField(verbose_name='path', max_length=255)
    description = models.TextField(verbose_name='des', max_length=610)
    like = models.IntegerField()
    createTime = models.DateTimeField()
    objects = PicManager()

    def __str__(self):
        return self.path


class MyUserManager(BaseUserManager):
    def _create_user(self, EmailAddress, username, password = None):
        if not EmailAddress:
            raise ValueError('The given EmailAddress must be set')
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(
            EmailAddress=self.normalize_email(EmailAddress),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, EmailAddress, username, password):
        user = self._create_user(EmailAddress,
            password=password,
            username = username)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Login(AbstractBaseUser, PermissionsMixin):
    EmailAddress = models.EmailField(verbose_name='email address',max_length=255, unique=True)
    username = models.TextField(verbose_name='username',max_length=255, unique=True)
    userpic = models.TextField(verbose_name='userpic', max_length=255, unique=True, blank=True,null=True)
    path = models.TextField(verbose_name='path', max_length=255, unique=True, blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'EmailAddress'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return self.EmailAddress

    def get_short_name(self):
        return self.EmailAddress

    def __str__(self):  # __unicode__ on Python 2
        return self.EmailAddress

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
