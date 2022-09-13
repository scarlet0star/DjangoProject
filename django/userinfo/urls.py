from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("",views.userView, name= "user"),
    path("login/",views.LoginView.as_view(), name="login"),
    path("logout/",views.logoutView, name= "logout"),
    path("signup/",views.UserSignUpView.as_view(), name= "signup"),
    path("edit/<str:username>",views.UserUpdateInfo.as_view(), name="update"),
    path("edit/<str:username>/pw",views.UserUpdatePW.as_view(), name="updatePW"),
    path("edit/<str:username>/off",views.UserUpdateOFF.as_view(), name="off"),
    path("<str:nickname>",views.UserInfoView.as_view(), name="userInfo"),
]
