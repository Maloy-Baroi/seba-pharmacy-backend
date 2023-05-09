"""
URL configuration for ims_backend project.

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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Before deploying the project we should change the path
    path('api-auth/', include('App_login.urls')),
    path('api-admin/', include('App_admin.urls')),
    path('api-seller/', include('App_seller.urls')),
    path('api-product/', include('App_products.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Define the custom 404 view function
def custom_404_view(request, exception):
    return views.render_custom_404(request)


# Register the custom 404 view as the handler for 404 errors
handler404 = custom_404_view
