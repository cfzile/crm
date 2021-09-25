from django import forms
from django.contrib.auth.models import User

from crm.constance import GRADE_TEMPLATE_TYPES_LIST, ROLE_LIST, PROTOTYPE_LIST
from crm.models import GradeTemplate


class UserForm(forms.ModelForm):
    username = forms.CharField(label='', help_text='', widget=forms.TextInput(attrs={'placeholder': 'username/email'}))
    name = forms.CharField(label='', help_text='', widget=forms.TextInput(attrs={'placeholder': 'ФИО'}))
    password = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Пароль', 'type': 'password'}))
    password_repeat = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Повторите пароль', 'type': 'password'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'e-mail'}))
    user_type = forms.ChoiceField(label='Роль', choices=ROLE_LIST, widget=forms.Select)
    prototype = forms.ChoiceField(label='Прототип', choices=PROTOTYPE_LIST, widget=forms.Select)
    user_position = forms.CharField(label='',
                                    widget=forms.TextInput(attrs={'placeholder': 'Должность'}))

    # user_departament = forms.CharField(label='',
    #                                    widget=forms.TextInput(attrs={'placeholder': 'Должность'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_repeat')


class GraderForm(forms.ModelForm):
    name = forms.CharField(label='Название', help_text='', widget=forms.TextInput(attrs={'placeholder': 'название'}))
    type = forms.ChoiceField(label='Тип', choices=GRADE_TEMPLATE_TYPES_LIST, widget=forms.Select)

    class Meta:
        model = GradeTemplate
        fields = ('name', 'type',)
