from .views import RegisterView, LoginView, IndexView, LogoutView
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("home/", views.home, name="home"),
    path('', IndexView.as_view(), name='index'),  # Swap the order of login/ and ''
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
