from django import forms
from store.models import Category, SubCategory, Attribute, AttributeChild, Shop, Aditions

# form category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


# form subcategory

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'description', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


# form attribute
class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


# form attribute child
class AttributeChildForm(forms.ModelForm):
    class Meta:
        model = AttributeChild
        fields = ['name', 'atribute']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'atribute': forms.Select(attrs={'class': 'form-control'}),
        }

# form shop


class ShopForm(forms.ModelForm):

    querysubcategory = SubCategory.objects.filter(category__name='restaurante')
    subcategory = forms.ModelMultipleChoiceField(
        queryset=querysubcategory, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Shop
        fields = ['name', 'manager', 'phone', 'address', 'description',
                  'image', 'category', 'subcategory']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


# form aditions
class AditionsForm(forms.ModelForm):
    class Meta:
        model = Aditions
        fields = ['name', 'price', 'shop']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'shop': forms.Select(attrs={'class': 'form-control'}),
        }
