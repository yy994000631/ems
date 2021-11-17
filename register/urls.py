from django.urls import path

from register import views

urlpatterns = [
	path('select/',views.select),
	path("register/", views.register),
	path("login/", views.login),
	path('receive_login/',views.receive_login),
	path('receive_register/',views.receive_register),
	path('index/',views.index),
	path('captcha/',views.get_captcha),
]