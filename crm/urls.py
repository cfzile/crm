from django.contrib import admin
from django.urls import path

from crm import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('id<int:user_id>', views.profile, name='profile'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_out', views.sign_out, name='sign_out'),
]
