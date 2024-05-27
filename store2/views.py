from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib import messages
from store.models import Category, SubCategory
from store2.forms import CategoryForm, SubcategoryForm

# Create your views here.


# vistas para categorias

class ListaCategorias(ListView):
    model = Category
    template_name = 'store2/lista-categorias.html'
    context_object_name = 'categorias'


class CrearCategoria(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'store2/crear-categoria.html'
    success_url = reverse_lazy('store2:lista-categorias')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('nombre')
        if Category.objects.filter(name=name).exists():
            messages.error(request, 'La categoría ya existe')
            return redirect('store:crear-categoria')
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Categoría creada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear la categoría')
        return super().form_invalid(form)


class EliminarCategoria(DeleteView):
    model = Category
    template_name = 'store2/eliminar-categoria.html'
    success_url = reverse_lazy('store2:lista-categorias')

    def form_valid(self, form):
        messages.success(self.request, 'Categoría eliminada correctamente')
        return super().form_valid(form)


class ActualizarCategoria(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'store2/actualizar-categoria.html'
    success_url = reverse_lazy('store2:lista-categorias')

    def form_valid(self, form):
        messages.success(self.request, 'Categoría actualizada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar la categoría')
        return super().form_invalid(form)


# vistas para subcategorias

# lista de subcategorias
class ListaSubCategorias(ListView):
    model = SubCategory
    template_name = 'store2/lista-subcategorias.html'
    context_object_name = 'subcategorias'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return SubCategory.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

# crear subcategoria


class CrearSubCategoria(CreateView):
    model = SubCategory
    form_class = SubcategoryForm
    template_name = 'store2/crear-subcategoria.html'
    success_url = reverse_lazy('store2:lista-categorias')

    def dispatch(self, *args, **kwargs):
        # Verifica que la categoría existe
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['category'] = self.category
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(
            pk=self.category.pk)
        form.fields['category'].initial = self.category
        form.fields['category'].widget.attrs['readonly'] = True
        return form

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        if SubCategory.objects.filter(name=name).exists():
            messages.error(request, 'La subcategoría ya existe')
            return redirect('store2:crear-subcategoria', slug=self.kwargs['slug'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.category = self.category
        messages.success(self.request, 'Subcategoría creada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear la subcategoría')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, slug=self.kwargs['slug'])
        return context
