from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager

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
    uploadedFile = models.FileField(upload_to="image/", default="NULL")

    def __str__(self):
        return f"Photo: {self.name}"

class Videos(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='videos')
    name = models.CharField(max_length=200, null=False)
    uploadedFile = models.FileField(upload_to="Videos/", default="NULL")

    def __str__(self):
        return f"Video: {self.name}"
