from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('protected', views.some_protected_view, name='protected'),  # Vista protegida
    path('login', views.user_login, name='login'),


]
