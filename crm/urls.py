from django.contrib import admin
from django.urls import path

from crm import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('id<int:user_id>', views.profile, name='profile'),
    path('grade<int:test_id>', views.get_grade, name='get_grade'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('add_grader', views.add_grader, name='add_grader'),
    path('add_competence', views.add_competence, name='add_competence'),
    path('create_task', views.create_task, name='create_task'),
    path('schedule_test', views.schedule_test, name='schedule_test'),
    path('pass_grade', views.pass_grade, name='pass_grade'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('tasks', views.tasks, name='tasks'),
    path('grade', views.grade, name='grade'),
    path('subordinates', views.subordinates, name='subordinates'),
    path('grade_templates', views.grade_templates, name='grade_templates'),
    path('add_subordinate', views.add_subordinate, name='add_subordinate'),
]
