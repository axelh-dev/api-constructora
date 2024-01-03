from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import  municipalidad, Projects, Photos, Videos, userrole
from .serializer import  UserLoginSerializer,UserRegisterSerializer, UserSerializer, MunicipalidadSerializer, ProjectsSerializer, PhotosSerializer, VideosSerializer, UserroleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import  login, logout, authenticate
from rest_framework import permissions, status
from .validations import custom_validation, validate_username, validate_password
from rest_framework.exceptions import ValidationError

@csrf_exempt
@require_POST
def cargar_archivo(request, tipo_archivo):
    data = JSONParser().parse(request)

    # Determina el tipo de archivo (photo o video)
    if tipo_archivo == 'photo':
        serializer = PhotosSerializer(data=data)
    elif tipo_archivo == 'video':
        serializer = VideosSerializer(data=data)  # Corrección aquí
    else:
        return JsonResponse({'error': 'Tipo de archivo no válido'})

    if serializer.is_valid():
        id_project = data.get('id_project')
        if id_project:
            project = Projects.objects.get(pk=id_project)
            serializer.save(id_project=project)
        else:
            return JsonResponse({'error': 'El campo id_project es requerido'})
        return JsonResponse(serializer.data)
    else:
        return JsonResponse(serializer.errors, status=400)

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)

        if serializer.is_valid(raise_exception=True):
            # Asegúrate de que 'create' devuelva una instancia de usuario
            user = serializer.save()

            # Accede al rol a través de la relación ForeignKey
            role = user.role_id.descrip_role if user.role_id else None

            # Accede a la descripción del municipio a través de la relación ForeignKey
            municipio = user.munici_id.name if user.munici_id else None

            if user:
                return Response({'user': user.username, 'role': role, 'municipio': municipio}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        assert validate_username(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=data['username'], password=data['password'])
           
            if user is not None:
                login(request, user)
                role = user.role_id.descrip_role if user.role_id else None

                municipio = user.munici_id.name if user.munici_id else None
                municipio_id = user.munici_id.munici_id if user.munici_id else None
                return Response({'user': user.username, 'role': role, 'municipio': municipio, 'Muni_id': municipio_id}, status=status.HTTP_200_OK)
            else:
                raise ValidationError('Usuario no encontrado o contraseña incorrecta')	


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)

# Create your views here.
class MunicipalidadViewSet(viewsets.ModelViewSet):
    queryset = municipalidad.objects.all()
    serializer_class = MunicipalidadSerializer
    
class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = userrole.objects.all()
    serializer_class = UserroleSerializer

class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer

def ProyectMuni(request, municipio_id):
    proyectos = Projects.objects.filter(munici_id=municipio_id)
    
    serializer = ProjectsSerializer(proyectos, many=True)
    proyectos_json = serializer.data

    if proyectos.exists():
        return JsonResponse(proyectos_json, safe=False)
    else:
        return JsonResponse({'mensaje': 'No se encontraron proyectos para el municipio especificado.'})


def videosProyect(request, projecto_id):
    videos = Videos.objects.filter(project_id= projecto_id)
    
    serializer = VideosSerializer(videos, many=True)
    videos_json = serializer.data

    if videos.exists():
        return JsonResponse(videos_json, safe=False)
    else:
        return JsonResponse({'mensaje': 'No se encontraron videos para el proyecto especificado.'})

def photosProyect(request, projecto_id):
    photos = Photos.objects.filter(project_id= projecto_id)
    
    serializer = PhotosSerializer(photos, many=True)
    photos_json = serializer.data

    if photos.exists():
        return JsonResponse(photos_json, safe=False)
    else:
        return JsonResponse({'mensaje': 'No se encontraron imagenes para el proyecto especificado.'})


class PhotosViewSet(viewsets.ModelViewSet):
    queryset = Photos.objects.all()
    serializer_class = PhotosSerializer

class VideosViewSet(viewsets.ModelViewSet):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer