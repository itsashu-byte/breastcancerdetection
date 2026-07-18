from django.urls import path
from . import views

urlpatterns = [

    # Home page
    path('', views.index, name='home'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('upload/', views.upload_mammogram, name='upload_mammogram'),
]