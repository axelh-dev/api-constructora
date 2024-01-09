from rest_framework import serializers
from .models import AppUser, municipalidad, Projects, Photos, Videos, userrole
from django.contrib.auth import  authenticate
from django.core.files.storage import default_storage
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from botocore.exceptions import ClientError
import logging
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

#UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('username', 'password', 'role_id', 'munici_id')

    def create(self, validated_data):
        # Extrae 'role_id' y 'munici_id' del diccionario validado
        role_id = validated_data.pop('role_id', None)
        munici_id = validated_data.pop('munici_id', None)

        # Crea el usuario sin asignar 'role_id' y 'munici_id' por ahora
        user_obj = AppUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        # Asigna 'role_id' si se proporciona
        if role_id:
            user_obj.role_id = role_id

        # Asigna 'munici_id' si se proporciona
        if munici_id:
            user_obj.munici_id = munici_id

        user_obj.save()  # Guarda el usuario con las asignaciones de llaves foráneas

        return user_obj

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def check_user(self, cleaned_data):
        user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
        if not user:
            raise ValidationError('Usuario no encontrado o contraseña incorrecta')
        return {'user': user, 'role': user.role}
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('username', 'password', 'role_id')


class MunicipalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = municipalidad
        fields = '__all__'

    @receiver(pre_delete, sender=municipalidad)
    def eliminar_archivo_s3_municipalidad(sender, instance, **kwargs):
     if instance.uploadedFile.name:
        try:
            default_storage.delete(instance.uploadedFile.name)
        except ClientError as e:
            logger.error(f"Error deleting file from S3: {e}")       

class UserroleSerializer(serializers.ModelSerializer):
    class Meta:
        model = userrole
        fields = '__all__'

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'

class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = '__all__'

    @receiver(pre_delete, sender='tasks.Photos')
    def eliminar_archivo_s3_photo(sender, instance, **kwargs):
     if instance.uploadedFile.name:
        try:
            default_storage.delete(instance.uploadedFile.name)
        except ClientError as e:
            logger.error(f"Error deleting file from S3: {e}")
class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = '__all__'

    @receiver(pre_delete, sender='tasks.Videos')
    def eliminar_archivo_s3_video(sender, instance, **kwargs):
     if instance.uploadedFile.name:
        try:
            default_storage.delete(instance.uploadedFile.name)
        except ClientError as e:
            logger.error(f"Error deleting file from S3: {e}")
