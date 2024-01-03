from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from .views import MunicipalidadViewSet, ProjectsViewSet, PhotosViewSet, VideosViewSet, cargar_archivo, UserRoleViewSet
from . import views
#api versioning 

router = routers.DefaultRouter()

# Registra tus vistas con el enrutador
router.register(r'municipalidades', MunicipalidadViewSet)
router.register(r'projects', ProjectsViewSet)
router.register(r'photos', PhotosViewSet)
router.register(r'videos', VideosViewSet)
router.register(r'roles', UserRoleViewSet)


urlpatterns = [
    path('v1/', include(router.urls) ),
    path('docs/', include_docs_urls(title="Api Constructora")),
    path('api/cargar_archivo/<str:tipo_archivo>/', cargar_archivo, name='cargar_archivo'),
    path('municipalidadf/<int:municipio_id>/', views.ProyectMuni, name='Filtro_muni'),
    path('proyectosfv/<int:projecto_id>/', views.videosProyect, name='Filtro_video'),
    path('proyectosfp/<int:projecto_id>/', views.photosProyect, name='Filtro_photos'),
    path('register/', views.UserRegister.as_view(), name='register'),
	path('login/', views.UserLogin.as_view(), name='login'),
	path('logout/', views.UserLogout.as_view(), name='logout'),
	path('user/', views.UserView.as_view(), name='user'),
    
]
