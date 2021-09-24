import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

import crm.events as events
from crm import constance
from crm.forms import UserForm
from crm.models import Profile

logger = logging.getLogger('crm')


def get_full_context(request, context):
    auth_profile = None
    if request.user.is_authenticated and request.user.is_superuser and Profile.objects.filter(
            user_id=request.user.id).count() == 0:
        Profile.objects.create(user=request.user).save()
    if request.user.is_authenticated:
        auth_profile = Profile.objects.get(user_id=request.user.id)
    general_context = {"events": events.get(request), 'constance': constance, 'auth_profile': auth_profile}
    return {**context, **general_context}


def home(request):
    return redirect('sign_in')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/')

    user_form = UserForm()

    if request.method == 'POST':

        user_form = UserForm(request.POST)

        if user_form.is_valid():

            if request.POST.get('password') == request.POST.get('password_repeat'):
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                Profile.objects.create(user=user, user_type=request.POST.get('user_type'),
                                       user_position=request.POST.get('user_position'))

                events.add_event(request, {constance.EVENT_INFO: ['Регистация прошла успешно.']})

                return redirect("sign_in")
            else:
                events.add_event(request, {constance.EVENT_ERROR: ['Пароли не совпадают.']})

        else:
            events.add_event(request, user_form.errors)

    return render(request, "pages/sign_up.html", get_full_context(request, {'Title': constance.SITE_SIGN_UP_NAME,
                                                                            'user_form': user_form}))


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/id' + str(request.user.id))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            events.add_event(request, {constance.EVENT_ERROR: [constance.NON_CORRECT_DATA]})

    template = loader.get_template('pages/sign_in.html')
    return HttpResponse(template.render(get_full_context(request, {'Title': constance.SITE_SIGN_IN_NAME}), request))


@login_required(login_url='/sign_in')
def sign_out(request):
    logout(request)
    return redirect('/')


def handler404(request, exception):
    response = render(request, 'pages/404.html', {})
    response.status_code = 404
    return response

@login_required(login_url='/sign_in')
def profile(request, user_id):
    profile = Profile.objects.get(user_id=user_id)
    print(user_id, profile.user.username)
    return render(request, "pages/profile.html", get_full_context(request, {'Title': profile.user.username}))
