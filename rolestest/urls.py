from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm
from .views import ActiveMenuList
from django.urls import path, reverse_lazy, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="authentication/login.html",
                                                         authentication_form=UserLoginForm,
                                                         redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('customer/menu/', ActiveMenuList.as_view(), name='menu_list'),
    path('api/v1/menu/', views.MenuList.as_view(), name='active_menu_list'),
]