from django.urls import path

from . import views

app_name = 'quotes'  ## allows for quotes:detail or quotes:archive reference
urlpatterns = [
    path('home/', views.IndexView.as_view(), name='index'),
    path('archive/', views.ArchiveView.as_view(), name='archive'),
    path('archive/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('login', views.LoginInterfaceView.as_view(), name='login'),
    path('logout/', views.LogoutInterfaceView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('history_bna/', views.BNAHistory.as_view(), name='history_bna'),
    path('history_bbva/', views.BBVAHistory.as_view(), name='history_bbva'),
    path('history_blue/', views.BlueHistory.as_view(), name='history_blue'),
    path('history_santander/', views.SantanderHistory.as_view(), name='history_santander'),
    path('history_patagonia/', views.PatagoniaHistory.as_view(), name='history_patagonia'),
    path('history_cop/', views.COPHistory.as_view(), name='history_cop'),
]
