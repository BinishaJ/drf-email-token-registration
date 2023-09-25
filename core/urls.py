from django.urls import path,include
from . import views

urlpatterns = [
    path("register/",views.RegisterView.as_view(), name='register-users'),
    path("verify/",views.VerifyView.as_view(), name='verify-users'),
    path("get-info/",views.InfoView.as_view(), name='info'),
]
