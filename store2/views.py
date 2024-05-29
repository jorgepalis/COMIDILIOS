from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib import messages
from store.models import Category, SubCategory, Attribute, AttributeChild, Shop, Aditions, Item, Variation, VariationValue, VARIATION_CHOICES
from store2.forms import CategoryForm, SubcategoryForm, AttributeForm, AttributeChildForm, ShopForm, ItemForm, AditionsForm, VariationForm, VariationValueForm

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


# vistas tiendas

# lista de tiendas
class ListaTiendas(ListView):
    model = Shop
    template_name = 'store2/lista-tiendas.html'
    context_object_name = 'tiendas'


# gestion de tiendas

def gestion_tienda(request, slug):
    tienda = get_object_or_404(Shop, slug=slug)
    context = {
        'tienda': tienda
    }
    return render(request, 'store2/gestion-tienda.html', context)

# actualizar tienda


class ActualizarTienda(UpdateView):
    model = Shop
    template_name = 'store2/actualizar-tienda.html'
    form_class = ShopForm

    def get_success_url(self):
        return reverse_lazy('store2:gestion-tienda', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        messages.success(self.request, 'Tienda actualizada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar la tienda')
        return super().form_invalid(form)


# vistas para adiciones

# lista de adiciones
class ListaAdiciones(ListView):
    model = Aditions
    template_name = 'store2/lista-adiciones.html'
    context_object_name = 'adiciones'

    def get_queryset(self):
        self.shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        return Aditions.objects.filter(shop=self.shop)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop'] = self.shop
        return context

# crear adiciones


class CrearAdicion(CreateView):
    model = Aditions
    template_name = 'store2/crear-adiciones.html'
    fields = ['name', 'price', 'shop']

    def get_success_url(self):
        return reverse_lazy('store2:lista-adiciones', kwargs={'slug': self.kwargs['slug']})

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        if Aditions.objects.filter(name=name).exists():
            messages.error(request, 'La adición ya existe')
            return redirect('store2:crear-adiciones')
        return super().post(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        initial['shop'] = shop
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        form.fields['shop'].queryset = Shop.objects.filter(pk=shop.pk)
        form.fields['shop'].initial = shop
        form.fields['shop'].widget.attrs['readonly'] = True
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Adición creada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear la adición')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop'] = get_object_or_404(Shop, slug=self.kwargs['slug'])
        return context

# eliminar adiciones

# editar adiciones

# vistas para items

# crear items


class CrearItem(CreateView):
    model = Item
    template_name = 'store2/crear-item.html'
    form_class = ItemForm

    def get_success_url(self):
        return reverse_lazy('store2:gestion-tienda', kwargs={'slug': self.kwargs['slug']})

    def dispatch(self, *args, **kwargs):
        # Verifica que la tienda existe
        self.shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['shop'] = self.shop
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['shop'].queryset = Shop.objects.filter(pk=self.shop.pk)
        form.fields['shop'].initial = self.shop
        form.fields['shop'].widget.attrs['readonly'] = True
        return form

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        if Item.objects.filter(name=name).exists():
            messages.error(request, 'El item ya existe')
            return redirect('store2:crear-item', slug=self.kwargs['slug'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Item creado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el item')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop'] = get_object_or_404(Shop, slug=self.kwargs['slug'])
        return context

# editar items


class ActualizarItem(UpdateView):
    model = Item
    template_name = 'store2/actualizar-item.html'
    form_class = ItemForm

    def get_success_url(self):
        return reverse_lazy('store2:gestion-tienda', kwargs={'slug': self.object.shop.slug})

    def form_valid(self, form):
        messages.success(self.request, 'Item actualizado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al actualizar el item')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop'] = get_object_or_404(Shop, slug=self.object.shop.slug)
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['shop'].disabled = True
        return form

# eliminar items


class EliminarItem(DeleteView):
    model = Item
    template_name = 'store2/eliminar-item.html'

    def get_success_url(self):
        return reverse_lazy('store2:gestion-tienda', kwargs={'slug': self.object.shop.slug})

    def form_valid(self, form):
        messages.success(self.request, 'Item eliminado correctamente')
        return super().form_valid(form)


# vistas para variaciones

# lista de variaciones
class ListaVariaciones(ListView):
    model = Variation
    template_name = 'store2/lista-variaciones.html'
    context_object_name = 'variaciones'

    def get_queryset(self):
        self.item = get_object_or_404(Item, slug=self.kwargs['slug'])
        return Variation.objects.filter(item=self.item)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = self.item
        return context


# crear variaciones
class CrearVariacion(CreateView):
    model = Variation
    template_name = 'store2/crear-variacion.html'
    form_class = VariationForm

    def get_success_url(self):
        return reverse_lazy('store2:lista-variaciones', kwargs={'slug': self.kwargs['slug']})

    def dispatch(self, *args, **kwargs):
        # Verifica que el item existe
        self.item = get_object_or_404(Item, slug=self.kwargs['slug'])
        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['item'] = self.item
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['item'].queryset = Item.objects.filter(pk=self.item.pk)
        form.fields['item'].initial = self.item
        form.fields['item'].widget.attrs['readonly'] = True
        return form

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        if Variation.objects.filter(name=name, item=self.item).exists():
            messages.error(request, 'La variación ya existe')
            return redirect('store2:crear-variacion', slug=self.kwargs['slug'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Variación creada correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear la variación')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = get_object_or_404(Item, slug=self.kwargs['slug'])
        return context


# valores variaciones
class ValoresVariacion(ListView):
    model = VariationValue
    template_name = 'store2/lista-valores-variacion.html'
    context_object_name = 'valores'

    def get_queryset(self):
        self.variation = get_object_or_404(Variation, pk=self.kwargs['pk'])
        return VariationValue.objects.filter(variation=self.variation)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variation'] = self.variation
        return context

# crear valores de variaciones


class CrearValorVariacion(CreateView):
    model = VariationValue
    template_name = 'store2/crear-valor-variacion.html'
    form_class = VariationValueForm

    def get_success_url(self):
        return reverse_lazy('store2:lista-valores-variacion', kwargs={'pk': self.kwargs['pk']})

    def dispatch(self, *args, **kwargs):
        # Verifica que la variación existe
        self.variation = get_object_or_404(Variation, pk=self.kwargs['pk'])
        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['variation'] = self.variation
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['variation'].queryset = Variation.objects.filter(
            pk=self.variation.pk)
        form.fields['variation'].initial = self.variation
        form.fields['variation'].widget.attrs['readonly'] = True
        form.fields['value'].queryset = AttributeChild.objects.filter(
            atribute=self.variation.attribute)
        return form

    def post(self, request, *args, **kwargs):
        value = request.POST.get('value')
        if VariationValue.objects.filter(value=value, variation=self.variation).exists():
            messages.error(request, 'El valor de la variación ya existe')
            return redirect('store2:crear-valor-variacion', pk=self.kwargs['pk'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request, 'Valor de la variación creado correctamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear el valor de la variación')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variation'] = get_object_or_404(
            Variation, pk=self.kwargs['pk'])
        return context


# ver producto completo
def ver_producto(request, slug):
    item = get_object_or_404(Item, slug=slug)
    context = {
        'item': item
    }
    return render(request, 'store2/producto-completo.html', context)
