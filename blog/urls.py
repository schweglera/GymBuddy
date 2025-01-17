from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.article_list, name="article_list"),
    path("article/<int:pk>/", views.article_detail, name="article_detail"),
    path("article/new/", views.add_article, name="add_article"),
    #-----------------
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('workouts/', views.all_workouts, name='all_workouts'),
    path('workout/create/', views.workout_create, name='workout_create'),
    path('workout/<int:pk>/', views.workout_detail, name='workout_detail'),
    path('coach/shop/', views.coach_shop, name='coach_shop'),
    path('trainingsplan/create/', views.tplan_create, name='tplan_create'),
    path('trainingsplaene/', views.tplan, name='all_tplan'),
    path('trainingsplan/<int:pk>/', views.tplan_detail, name='tplan_detail'),
]



