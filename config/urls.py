from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin







urlpatterns = [

    path("users/", include("users.urls")),
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls'))

]
