from django.urls import path
from . import views

app_name = 'store2'

urlpatterns = [
    path('lista-categorias/', views.ListaCategorias.as_view(),
         name='lista-categorias'),
    path('crear-categoria/', views.CrearCategoria.as_view(), name='crear-categoria'),
    path('eliminar-categoria/<int:pk>/',
         views.EliminarCategoria.as_view(), name='eliminar-categoria'),
    path('actualizar-categoria/<int:pk>/',
         views.ActualizarCategoria.as_view(), name='actualizar-categoria'),

    path('lista-subcategorias/<slug>/',
         views.ListaSubCategorias.as_view(), name='lista-subcategorias'),
    path('crear-subcategoria/<slug>/', views.CrearSubCategoria.as_view(),
         name='crear-subcategoria'),
    path('eliminar-subcategoria/<slug>/',
         views.EliminarSubCategoria.as_view(), name='eliminar-subcategoria'),
    path('actualizar-subcategoria/<slug>/',
         views.ActualizarSubCategoria.as_view(), name='actualizar-subcategoria'),
]
