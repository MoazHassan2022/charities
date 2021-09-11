from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("النتائج", views.results, name="results"),
    path("charity/<str:name>", views.charityPage, name="charityPage"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register/<str:accessCode>", views.register, name="register"),
    path("create", views.createPage, name="create"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("send", views.sendEmails, name="send")
]