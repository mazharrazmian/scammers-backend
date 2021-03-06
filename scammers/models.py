from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password. 
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)   

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)





class Scammer(models.Model):
    first_name = models.CharField("First Name",max_length=100)
    last_name = models.CharField("Last Name", max_length=100)
    phone = models.CharField("Phone Number",max_length=13)
    address = models.CharField("Address",max_length=200)
    title = models.CharField("Title",max_length=100)
    details = models.TextField(null=True,help_text="Add details about the incident")
    posted_by = models.ForeignKey(User,related_name="scammers_posted",on_delete=models.DO_NOTHING,default="Mazhar Ali")
    created_at = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'






def buyer_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/scam_images/scammer_name /<filename>
    return f'scam_images/{instance.scammer.id}/{filename}'



class Images(models.Model):
    image = models.ImageField("Upload the image proofs if you have any",upload_to=buyer_directory_path,blank=True,null=True)
    scammer = models.ForeignKey('Scammer', on_delete=models.CASCADE,related_name="image_proofs")
    
