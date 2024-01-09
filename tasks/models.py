from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage

#import logging
#logger = logging.getLogger(__name__)

def upload_to(instance, filename):
    return f'{instance.__class__.__name__.lower()}s/{filename}'

class AppUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El campo de nombre de usuario debe establecerse')
        if not password:
            raise ValueError('La contraseña es obligatoria.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)



class municipalidad(models.Model):
    munici_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    uploadedFile = models.FileField(upload_to="image/", default="NULL")
    
    def __str__(self):
        return f"User: {self.name}"
    
    # def eliminar_archivo_s3_municipalidad(self):
    #     if self.uploadedFile.name:
    #         try:
    #             default_storage.delete(self.uploadedFile.name)
    #         except Exception as e:
    #             logger.error(f"Error deleting file from S3: {e}")

    #     super().delete()

class userrole(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    descrip_role = models.CharField(max_length=20, null=False)
    
    def __str__(self):
        return f"User: {self.name}"

class AppUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    role_id = models.ForeignKey(userrole, on_delete=models.CASCADE, default=1)
    munici_id = models.ForeignKey(municipalidad, on_delete=models.CASCADE, default=None, null=True)
    is_staff = models.BooleanField(default=False)
    objects = AppUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    # Especifica nombres de acceso inverso únicos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='appuser_groups',
        related_query_name='appuser_group',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='appuser_user_permissions',
        related_query_name='appuser_user_permission',
        blank=True,
    )

    def __str__(self):
        return self.username


class Projects(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    munici_id = models.ForeignKey(municipalidad, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50, null=False)
    nog = models.CharField(max_length=50, null=False,   unique=True ,default=1)
    date = models.DateField(null=True)

    def __str__(self):
        return f"Project: {self.name}"

class Photos(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='photos')
    name = models.CharField(max_length=200, null=False)
    uploadedFile = models.FileField(upload_to="image/", null=True)

    def __str__(self):
        return f"Photo: {self.name}"

    # @receiver(pre_delete, sender='tasks.Photos')
    # def eliminar_archivo_s3_photo(sender, instance, **kwargs):
    #  if instance.uploadedFile.name:
    #     try:
    #         default_storage.delete(instance.uploadedFile.name)
    #     except Exception as e:
    #         logger.error(f"Error deleting file from S3: {e}")


class Videos(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='videos')
    name = models.CharField(max_length=200, null=False)
    uploadedFile = models.FileField(upload_to="Videos/", null=True)

    def __str__(self):
        return f"Video: {self.name}"
    
    # @receiver(pre_delete, sender='tasks.Videos')
    # def eliminar_archivo_s3_video(sender, instance, **kwargs):
    #  if instance.uploadedFile.name:
    #     try:
    #         default_storage.delete(instance.uploadedFile.name)
    #     except Exception as e:
    #         logger.error(f"Error deleting file from S3: {e}")