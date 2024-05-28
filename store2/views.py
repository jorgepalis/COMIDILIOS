from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib import messages
from store.models import Category, SubCategory, Attribute, AttributeChild
from store2.forms import CategoryForm, SubcategoryForm, AttributeForm, AttributeChildForm

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
        name = request.POST.get('name')
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

    def get_success_url(self):
        return reverse_lazy('store2:lista-subcategorias', kwargs={'slug': self.kwargs['slug']})

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


# eliminar subcategoria
class EliminarSubCategoria(DeleteView):
    model = SubCategory
    template_name = 'store2/eliminar-subcategoria.html'

    def get_success_url(self):
        return reverse_lazy('store2:lista-subcategorias', kwargs={'slug': self.object.category.slug})

    def form_valid(self, form):
        messages.success(self.request, 'Subcategoría eliminada correctamente')
        return super().form_valid(form)


# actualizar subcategoria
class ActualizarSubCategoria(UpdateView):
    model = SubCategory
    form_class = SubcategoryForm
    template_name = 'store2/actualizar-subcategoria.html'

    def get_success_url(self):
        return reverse_lazy('store2:lista-subcategorias', kwargs={'slug': self.object.category.slug})

    def form_valid(self, form):
        messages.success(
            self.request, 'Subcategoría actualizada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar la subcategoría')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, slug=self.object.category.slug)
        return context


# vistas para atributos

# lista de atributos
class ListaAtributos(ListView):
    model = Attribute
    template_name = 'store2/lista-atributos.html'
    context_object_name = 'atributos'


# crear atributo
class CrearAtributo(CreateView):
    model = Attribute
    template_name = 'store2/crear-atributo.html'
    fields = ['name']
    success_url = reverse_lazy('store2:lista-atributos')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        if Attribute.objects.filter(name=name).exists():
            messages.error(request, 'El atributo ya existe')
            return redirect('store2:crear-atributo')
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Atributo creado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el atributo')
        return super().form_invalid(form)

# eliminar atributo


class EliminarAtributo(DeleteView):
    model = Attribute
    template_name = 'store2/eliminar-atributo.html'
    success_url = reverse_lazy('store2:lista-atributos')

    def form_valid(self, form):
        messages.success(self.request, 'Atributo eliminado correctamente')
        return super().form_valid(form)


# editar atributo
class ActualizarAtributo(UpdateView):
    model = Attribute
    template_name = 'store2/actualizar-atributo.html'
    fields = ['name']
    success_url = reverse_lazy('store2:lista-atributos')

    def form_valid(self, form):
        messages.success(self.request, 'Atributo actualizado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar el atributo')
        return super().form_invalid(form)


# vistas para atributos hijos

# lista de atributos hijos
class ListaAtributosHijos(ListView):
    model = AttributeChild
    template_name = 'store2/lista-atributos-hijos.html'
    context_object_name = 'hijos'

    def get_queryset(self):
        self.attribute = get_object_or_404(Attribute, slug=self.kwargs['slug'])
        return AttributeChild.objects.filter(atribute=self.attribute)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attribute'] = self.attribute
        return context

# crear atributo hijo


class CrearAtributoHijo(CreateView):
    model = AttributeChild
    template_name = 'store2/crear-atributo-hijo.html'
    form_class = AttributeChildForm

    def get_success_url(self):
        return reverse_lazy('store2:lista-atributos-hijos', kwargs={'slug': self.kwargs['slug']})

    def dispatch(self, *args, **kwargs):
        # Verifica que el atributo existe
        self.atribute = get_object_or_404(Attribute, slug=self.kwargs['slug'])
        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['atribute'] = self.atribute
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['atribute'].queryset = Attribute.objects.filter(
            pk=self.atribute.pk)
        form.fields['atribute'].initial = self.atribute
        form.fields['atribute'].widget.attrs['readonly'] = True
        return form

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        if AttributeChild.objects.filter(name=name).exists():
            messages.error(request, 'El atributo hijo ya existe')
            return redirect('store2:crear-atributo-hijo', slug=self.kwargs['slug'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.atribute = self.atribute
        messages.success(self.request, 'Atributo hijo creado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el atributo hijo')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attribute'] = get_object_or_404(
            Attribute, slug=self.kwargs['slug'])
        return context


# actualizar atributo hijo
class ActualizarAtributoHijo(UpdateView):
    model = AttributeChild
    template_name = 'store2/actualizar-atributo-hijo.html'
    form_class = AttributeChildForm

    def get_success_url(self):
        return reverse_lazy('store2:lista-atributos-hijos', kwargs={'slug': self.object.atribute.slug})

    def form_valid(self, form):
        messages.success(
            self.request, 'Atributo hijo actualizado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar el atributo hijo')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attribute'] = get_object_or_404(
            Attribute, slug=self.object.atribute.slug)
        return context


# eliminar atributo hijo
class EliminarAtributoHijo(DeleteView):
    model = AttributeChild
    template_name = 'store2/eliminar-atributo-hijo.html'

    def get_success_url(self):
        return reverse_lazy('store2:lista-atributos-hijos', kwargs={'slug': self.object.atribute.slug})

    def form_valid(self, form):
        messages.success(self.request, 'Atributo hijo eliminado correctamente')
        return super().form_valid(form)


# vistas para adiciones
