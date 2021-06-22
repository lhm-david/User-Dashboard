from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.registerpage),
    path('login', views.loginpage),
    path('registered', views.register),
    path('signin',views.login),
    path('success', views.inpage),
    path('addnew',views.addnewpage),
    path('create_user', views.addnewuser),
    path('userprofile/<int:user_id>', views.userpage),
    path('addmessage/<int:user_id>', views.addmessage),
    path('userprofile/<int:message_id>/addcomment', views.addcomment),
    path('userprofile/<int:user_id>/edit',views.edituserpage),
    path('edituser/<int:user_id>', views.edituser),
    path('logout', views.logout),
    path('userprofile/delete/<int:id>',views.delete)
]