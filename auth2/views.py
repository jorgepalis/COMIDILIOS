from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .forms import UserForm
from django.contrib import messages
from Auth.models import User

# Create your views here.


def es_admin(user):
    return user.is_authenticated and user.is_admin


# vista para crear usuarios
@user_passes_test(es_admin, login_url='auth2:login')
def crear_usuario(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente')
            return redirect('auth2:listar-usuario')
    return render(request, 'auth2/crear-usuario.html', {'form': form})

# vista para eliminar usuarios


@user_passes_test(es_admin, login_url='auth2:login')
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if 'confirmar' in request.POST:
            usuario.delete()
            messages.success(request, 'Usuario eliminado correctamente')
            return redirect('auth2:listar-usuarios')
        else:
            return redirect('productos:auth:listar-usuarios')
    return render(request, 'auth2/eliminar-usuario.html', {'usuario': usuario})

# vista para editar usuarios


@user_passes_test(es_admin, login_url='auth2:login')
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    form = UserForm(instance=usuario)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario editado correctamente')
            return redirect('auth2:listar-usuarios')
    return render(request, 'auth2/editar-usuario.html', {'form': form})


# vista para listar usuarios
@user_passes_test(es_admin, login_url='auth2:login')
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'auth2/lista-usuarios.html', {'usuarios': usuarios})
