"""
URL configuration for OPKCWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# Import the new view function from your visualization app
from visualization import views as visualization_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. New: Map the root URL ('') to your home_view
    path('', visualization_views.home_view, name='home'),
    
    # 2. Existing: Keep the 'charts/' prefix for your application URLs
    path('charts/', include('visualization.urls')),
]