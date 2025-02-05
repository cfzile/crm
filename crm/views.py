import logging

import plotly.graph_objs as go
from django.db.models import Q
from plotly.graph_objs.scatter import Marker
from plotly.offline import *

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

import crm.events as events
from crm import constance
from crm.constance import *
from crm.forms import UserForm, GraderForm
from crm.models import Profile, Competence, GradeTemplate, Question, Schedule, Indicator, Task, Answer, GradeResults

logger = logging.getLogger('crm')


def get_full_context(request, context):
    auth_profile = None
    scheduled_to_user = None
    scheduled_by_user = None

    if request.user.is_authenticated and request.user.is_superuser and Profile.objects.filter(
            user_id=request.user.id).count() == 0:
        Profile.objects.create(user=request.user).save()

    competences = Competence.objects.all()
    grade_templates = GradeTemplate.objects.all()
    tasks = None
    if request.user.is_authenticated:
        auth_profile = Profile.objects.get(user_id=request.user.id)
        auth_profile.subordinates = [Profile.objects.get(user_id=id) for id in auth_profile.subordinates]
        scheduled_to_user = Schedule.objects.all().filter(subordinate=auth_profile.user.id)
        scheduled_by_user = Schedule.objects.all().filter(owner=auth_profile.user.id)
        tasks = Task.objects.all().filter(Q(owner_id=request.user.id) | Q(executor_id=request.user.id))
        # print(auth_profile.prototype)
        # for com in competences:
        #     print(com.prototype)
        if auth_profile.prototype != -1:
            competences = competences.filter(Q(prototype=auth_profile.prototype))
            grade_templates = grade_templates.filter(Q(prototype=auth_profile.prototype))

    general_context = {"events": events.get(request),
                       'constance': constance,
                       'auth_profile': auth_profile,
                       'competences': competences,
                       'grade_templates': grade_templates,
                       'scheduled_to_user': scheduled_to_user,
                       'scheduled_by_user': scheduled_by_user,
                       'tasks': tasks,
                       'profiles': Profile.objects.all()}

    return {**context, **general_context}


def home(request):
    return redirect('sign_in')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/')

    user_form = UserForm()

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        user_form.username = request.POST.get('email')

        if user_form.is_valid():

            if request.POST.get('password') == request.POST.get('password_repeat'):
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                Profile.objects.create(user=user, name=request.POST.get('name'),
                                       user_type=request.POST.get('user_type'),
                                       prototype=request.POST.get('prototype'),
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
        password = request.POST.get('password')
        username = request.POST.get('username')
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
    requested_profile = Profile.objects.get(user_id=user_id)
    requested_profile.manager_profiles = [Profile.objects.get(user_id=id) for id in requested_profile.managers]
    requested_profile.subordinate_profiles = [Profile.objects.get(user_id=id) for id in requested_profile.subordinates]

    return render(request, "pages/profile.html",
                  get_full_context(request,
                                   {'Title': requested_profile.name,
                                    'requested_profile': requested_profile,
                                    'chosen_page': PROFILE_PAGE_NAME}))


def tasks(request):
    return render(request, "pages/tasks.html",
                  get_full_context(request, {'Title': 'Задачи', 'chosen_page': TASKS_PAGE_NAME}))


def grade(request):
    return render(request, "pages/grade.html",
                  get_full_context(request, {'Title': 'Оценка', 'chosen_page': TESTS_PAGE_NAME}))


def grade_templates(request):
    return render(request, "pages/grade_templates.html",
                  get_full_context(request, {'Title': 'Шаблоны',
                                             'create_grader_form': GraderForm(),
                                             'chosen_page': TEMPLATES_PAGE_NAME,
                                             'competences': Competence.objects.all()}))


def add_grader(request):
    if request.method == 'POST':
        prototype = Profile.objects.get(user_id=request.user.id).prototype
        if prototype == -1:
            prototype = request.POST.get('prototype')
        name = request.POST.get('name')
        type = request.POST.get('type')

        questions_dict = {i: [None, '', None] for i in range(100)}
        obj = GradeTemplate.objects.create(name=name, type=type,
                                           prototype=prototype,
                                           owner=Profile.objects.get(user_id=request.user.id))

        obj.score = 0

        for key in request.POST.keys():
            if key[:len('t1_q_')] == 't1_q_':
                ind = len('t1_q_')
                questions_dict[int(key[ind:])] = [1, request.POST.get('t1_q_' + key[ind:]), None]

            if key[:len('t2_q_')] == 't2_q_':
                ind = len('t2_q_')
                questions_dict[int(key[ind:])] = [2, '', int(request.POST.get('t2_q_' + key[ind:]))]
                obj.score += max([ind.value for ind in Competence.objects.get(
                    id=int(request.POST.get('t2_q_' + key[ind:]))).indicators.all()])

        for key, value in questions_dict.items():
            if value[0] is None:
                continue
            competence = None
            if value[2] is not None:
                competence = Competence.objects.get(id=value[2])
            obj.questions.add(Question.objects.create(type=value[0], description=value[1],
                                                      competence=competence))

        obj.save()

    return redirect('/grade_templates')


def add_competence(request):
    if request.method == 'POST':
        prototype = Profile.objects.get(user_id=request.user.id).prototype
        if prototype == -1:
            prototype = request.POST.get('prototype')
        name = request.POST.get('name')
        indicators = {i: [None, None] for i in range(0, 1 + len(request.POST.keys()) // 2)}

        for key in request.POST.keys():
            if key[:len('indicator_name')] == 'indicator_name':
                ind = len('indicator_name')
                indicators[int(key[ind:])][0] = request.POST.get('indicator_name' + key[ind:])
            if key[:len('indicator_value')] == 'indicator_value':
                ind = len('indicator_value')
                indicators[int(key[ind:])][1] = request.POST.get('indicator_value' + key[ind:])

        competence = Competence.objects.create(name=name, description='', prototype=prototype)

        for key, value in indicators.items():
            if value[0] is None or value[1] is None:
                continue  # TODO: error
            indicator = Indicator.objects.create(name=value[0], value=value[1])
            indicator.save()
            competence.indicators.add(indicator)

        competence.save()

    return redirect('/grade_templates')


def schedule_test(request):
    if request.method == 'POST':
        owner = request.user.id
        grade_template = request.POST.get('grade_template')
        subordinate = request.POST.get('subordinate')
        date_from = request.POST.get('from')
        date_to = request.POST.get('to')

        Schedule.objects.create(owner=owner, grade_template=GradeTemplate.objects.get(id=grade_template),
                                subordinate=subordinate, date_to=date_to,
                                date_from=date_from).save()

    return redirect('/grade')


def pass_grade(request):
    if request.method == 'POST':
        gt_id = request.POST.get('grade_template')
        results = GradeResults.objects.create(executor=Profile.objects.get(user_id=request.user.id),
                                              grade_template=GradeTemplate.objects.get(id=gt_id))
        score = 0
        for key in request.POST.keys():
            t1 = 'ans_'
            t2 = 'indicator_'
            if key[:len(t1)] == t1:
                q_id = key[len(t1):]
                answer = Answer.objects.create(question=Question.objects.get(id=q_id), answer_t1=request.POST.get(key))
                answer.save()
                results.answers.add(answer)

            if key[:len(t2)] == t2:
                q_id = key[len(t2):]
                indicator = Indicator.objects.get(id=request.POST.get(key))
                q = Question.objects.get(id=q_id)
                answer = Answer.objects.create(question=q,
                                               answer_t2=indicator)
                score += indicator.value
                # total += max([i.value for i in q.competence.indicators.all()])
                answer.save()
                results.answers.add(answer)

        sch = Schedule.objects.get(id=request.POST.get('schedule'))
        sch.status = 1
        results.schedule_id = sch.id

        if request.user.id == sch.owner:
            results.owner_score = score
            sch.owner_score = score
        if request.user.id == sch.subordinate:
            results.subordinate_score = score
            sch.subordinate_score = score

        sch.save()
        results.save()

    return redirect('grade')


def get_grade(request, test_id, scheduled=None):
    schedule = None
    pass_allow = False
    if scheduled is not None:
        schedule = Schedule.objects.filter(id=scheduled)
        if schedule.count() != 0:
            schedule = schedule[0]
            if schedule.owner == request.user.id or schedule.subordinate == request.user.id:
                if GradeResults.objects.all().filter(executor_id=request.user.id, schedule_id=schedule.id).count() == 0:
                    pass_allow = True
    return render(request, "pages/show_test.html",
                  get_full_context(request, {'Title': 'Пройдите тест',
                                             'grade': GradeTemplate.objects.get(id=test_id),
                                             'schedule': schedule,
                                             'pass_allow': pass_allow,
                                             'competences': Competence.objects.all()}))


def create_task(request):
    if request.method == 'POST':
        owner = request.user.id
        description = request.POST.get('description')
        executor = request.POST.get('subordinate')
        grade_template = request.POST.get('grade_template')
        date_from = request.POST.get('from')
        date_to = request.POST.get('to')

        grade_template_obj = None
        try:
            grade_template_obj = GradeTemplate.objects.get(id=grade_template)
        except:
            pass

        sch = Schedule.objects.create(grade_template=grade_template_obj, owner=owner, subordinate=executor,
                                      date_from=date_from, date_to=date_to)
        sch.save()

        Task.objects.create(owner=Profile.objects.get(user_id=owner), description=description,
                            grade_template=grade_template_obj,
                            executor=Profile.objects.get(user_id=executor), date_to=date_to,
                            date_from=date_from,
                            schedule_id=sch.id).save()

    return redirect('tasks')


def subordinates(request):
    return render(request, "pages/subordinates.html",
                  get_full_context(request, {'Title': 'Подчиненные', 'chosen_page': SUBORDINATES_PAGE_NAME}))


def add_subordinate(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user_id=request.user.id)
        subordinate = Profile.objects.get(user_id=request.POST.get('subordinate'))
        if subordinate.user.id not in set(profile.subordinates):
            profile.subordinates.append(subordinate.user.id)
        if request.user.id not in set(subordinate.managers):
            subordinate.managers.append(request.user.id)
        profile.save()
        subordinate.save()

    return redirect('/')


def get_report(request, schedule_id):
    try:
        sch = Schedule.objects.get(id=schedule_id)

        owner_id = sch.owner
        subordinate_id = sch.subordinate

        answer_ruk = GradeResults.objects.get(schedule_id=schedule_id, executor_id=owner_id)
        answer_sot = GradeResults.objects.get(schedule_id=schedule_id, executor_id=subordinate_id)

        fig = go.Figure()

        def get_scatter(answer, name):
            p = 1
            x, ruk_y = [], []
            for ans in answer.answers.all():
                if ans.answer_t2 is None:
                    continue
                x.append(p)
                ruk_y.append(ans.answer_t2.value)
                p += 1

            return go.Scatter(x=x, y=ruk_y,
                              mode='markers+lines',
                              marker=Marker(symbol='0'),
                              opacity=0.8, name=name)

        p = 1
        comps = []
        for ans in answer_sot.answers.all():
            if ans.answer_t2 is None:
                continue
            comps.append((p, ans.question.competence.name))
            p += 1

        fig.add_trace(get_scatter(answer_ruk, 'Руководитель'))
        fig.add_trace(get_scatter(answer_sot, 'Сотрудник'))

        plt_div = plot(fig, output_type='div')

        return render(request, "pages/report.html",
                      get_full_context(request, {'Title': 'Отчет',
                                                 'schedule': sch,
                                                 'answer_ruk': answer_ruk,
                                                 'answer_sot': answer_sot,
                                                 'graphic': plt_div,
                                                 'comps': comps}))

    except:
        events.add_event(request, {constance.EVENT_ERROR: ['Недостаточно данных']})

    return redirect('grade')
