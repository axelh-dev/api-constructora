from django.contrib.auth.models import User
from rest_framework import serializers
from .models import AppUser, municipalidad, Projects, Photos, Videos, userrole
from django.contrib.auth import get_user_model, authenticate

from rest_framework.exceptions import ValidationError

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

class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = '__all__'
