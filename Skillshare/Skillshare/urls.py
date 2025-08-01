"""
URL configuration for Skillshare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from core.models import UserProfile
UserProfile.objects.all()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='homepage'),
    path('success/',views.success,name='success'),
    path('auth/', include('social_django.urls', namespace='social')),

    path('core/',include('core.urls')),
    path('connect/',include('connect.urls')),

    path("",include("allauth.urls")),



    path("__reload__/", include("django_browser_reload.urls")), # auto reload.



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
