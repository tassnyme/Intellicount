"""
URL configuration for registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views 
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('signup/',views.SignupPage,name='signup'),
    # path('',views.LoginPage,name="login"),
    # path('home/',views.home,name='logout'),
    # path('user_profile/',views.user_profile,name='user_profile'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('Accounts/', views.account, name='account'),
    # path('dashboard_user/',views.user_dash , name= 'dashboard_user'),
    # path('Delete_users/(?P<pk>\d+)/',views.Deleteuser,name='Delete'),
    # path('update/(?P<pk>\d+)/',views.update,name='update'),
    # path('update_users/(?P<pk>\d+)/', views.updateuser, name='updateuser'),
    # path('updatprofile/(?P<pk>\d+)/', views.updatprofile, name='updatprofile'),
    # path('add_user/',views.AddUser,name='add_user'),
    # path('verify/(?P<pk>\d+)/',views.verify_user,name='verify'),
    path('index/',views.index),
    path('addd/',views.add_person),
    path('gett/',views.get_all_person),


]
