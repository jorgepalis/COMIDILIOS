from django import forms
from Auth.models import User

# creacion de usuarios


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_admin',
                  'is_vendor', 'is_client', 'is_rider', 'phone_num', 'image',]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
