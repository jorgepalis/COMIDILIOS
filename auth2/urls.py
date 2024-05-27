from django.urls import path
from django.contrib.auth import views as auth_views
from auth2 import views

app_name = 'auth2'

urlpatterns = [
    path('crear-usuario/', views.crear_usuario, name='crear-usuario'),
    path('login/', auth_views.LoginView.as_view(template_name='auth2/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('usuarios/', views.listar_usuarios, name='listar-usuarios'),
    path('eliminar-usuario/<int:pk>/',
         views.eliminar_usuario, name='eliminar-usuario'),
    path('editar-usuario/<int:pk>/', views.editar_usuario, name='editar-usuario'),
]
