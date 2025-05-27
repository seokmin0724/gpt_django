from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")),
]
