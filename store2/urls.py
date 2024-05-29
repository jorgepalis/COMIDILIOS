from django.urls import path
from . import views

app_name = 'store2'

urlpatterns = [
    # categorias
    path('lista-categorias/', views.ListaCategorias.as_view(),
         name='lista-categorias'),
    path('crear-categoria/', views.CrearCategoria.as_view(), name='crear-categoria'),
    path('eliminar-categoria/<slug>/',
         views.EliminarCategoria.as_view(), name='eliminar-categoria'),
    path('actualizar-categoria/<slug>/',
         views.ActualizarCategoria.as_view(), name='actualizar-categoria'),

    # subcategorias
    path('lista-subcategorias/<slug>/',
         views.ListaSubCategorias.as_view(), name='lista-subcategorias'),
    path('crear-subcategoria/<slug>/', views.CrearSubCategoria.as_view(),
         name='crear-subcategoria'),
    path('eliminar-subcategoria/<slug>/',
         views.EliminarSubCategoria.as_view(), name='eliminar-subcategoria'),
    path('actualizar-subcategoria/<slug>/',
         views.ActualizarSubCategoria.as_view(), name='actualizar-subcategoria'),

    # atributos
    path('lista-atributos/', views.ListaAtributos.as_view(), name='lista-atributos'),
    path('crear-atributo/', views.CrearAtributo.as_view(), name='crear-atributo'),
    path('eliminar-atributo/<slug>/',
         views.EliminarAtributo.as_view(), name='eliminar-atributo'),
    path('actualizar-atributo/<slug>/',
         views.ActualizarAtributo.as_view(), name='actualizar-atributo'),

    # atributos hijos
    path('lista-atributos-hijos/<slug>/',
         views.ListaAtributosHijos.as_view(), name='lista-atributos-hijos'),
    path('crear-atributo-hijo/<slug>/',
         views.CrearAtributoHijo.as_view(), name='crear-atributo-hijo'),
    path('eliminar-atributo-hijo/<pk>/',
         views.EliminarAtributoHijo.as_view(), name='eliminar-atributo-hijo'),
    path('actualizar-atributo-hijo/<pk>/',
         views.ActualizarAtributoHijo.as_view(), name='actualizar-atributo-hijo'),

    # tiendas
    path('lista-tiendas/', views.ListaTiendas.as_view(), name='lista-tiendas'),
    path('gestion-tienda/<slug>/', views.gestion_tienda, name='gestion-tienda'),
    path('actualizar-tienda/<slug>/',
         views.ActualizarTienda.as_view(), name='actualizar-tienda'),

    # adiciones
    path('lista-adiciones/<slug>/',
         views.ListaAdiciones.as_view(), name='lista-adiciones'),
    path('crear-adicion/<slug>/', views.CrearAdicion.as_view(), name='crear-adicion'),

    # items
    path('crear-item/<slug>/', views.CrearItem.as_view(), name='crear-item'),
    path('actualizar-item/<slug>/',
         views.ActualizarItem.as_view(), name='actualizar-item'),
    path('eliminar-item/<slug>/', views.EliminarItem.as_view(), name='eliminar-item'),

    # variaciones
    path('lista-variaciones/<slug>/',
         views.ListaVariaciones.as_view(), name='lista-variaciones'),
    path('crear-variacion/<slug>/',
         views.CrearVariacion.as_view(), name='crear-variacion'),

    # valores de variaciones
    path('lista-valores-variacion/<pk>/',
         views.ValoresVariacion.as_view(), name='lista-valores-variacion'),
    path('crear-valor-variacion/<pk>/',
         views.CrearValorVariacion.as_view(), name='crear-valor-variacion'),

    # producto completo
    path('producto/<slug>/', views.ver_producto, name='ver-producto'),
]
