from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(label='', help_text='', widget=forms.TextInput(attrs={'placeholder': 'ФИО'}))
    password = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Пароль', 'type': 'password'}))
    password_repeat = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Повторите пароль', 'type': 'password'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'e-mail'}))
    user_type = forms.ChoiceField(choices=[(0, 'сотрудник'), (1, 'клиент')], widget=forms.Select)
    user_position = forms.CharField(label='',
                                    widget=forms.TextInput(attrs={'placeholder': 'Должность'}))
    # user_departament = forms.CharField(label='',
    #                                    widget=forms.TextInput(attrs={'placeholder': 'Должность'}))

    class Meta:
        model = User
        fields = ('username', 'password', 'password_repeat', 'email')
