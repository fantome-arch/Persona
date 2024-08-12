"""persona URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from interface import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('signup/',views.signup,name='signup'),
    path('login/',views.user_login,name='login'),
    path('home/',views.home2,name='home'),
    path('logout/',views.log_out,name='logout'),
    path('writeentry/',views.diary_entry,name='entry'),
    path('entry/<str:user>',views.view_entries_list,name='viewentry'),
    path('entry/<str:user>/<int:no>',views.view_entries_list,name='showentry'),
    path('delete/<int:object>',views.deleteentry,name='delete_entry'),
    path('update/<int:object>',views.updateentry,name='update_entry'),
    path('verify/',views.account_verification,name='verify'),
    path('resend/',views.send_email,name='resend'),
    path('forgotpassword/',views.forgot_password,name='forgotpassword'),
    path('emailsent/<str:email>',views.pass_reset_email,name='resetpass'),

    
    



]
