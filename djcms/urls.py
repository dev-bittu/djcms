"""
URL configuration for djcms project.

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
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("blogs/", include("blogs.urls")),
    path("manage/", include("management.urls")),
    path("", views.Index.as_view(), name="index"),
    path("trendings/", views.Trendings.as_view(), name="trendings"),
    path("latest/", views.Latest.as_view(), name="latest"),
    path("popular/", views.Popular.as_view(), name="popular"),
    path("search/<str:query>/", views.Search.as_view(), name="search"),
    path("category/", views.Category.as_view(), name="category"),
    path("category/<str:cat>/", views.GetCategory.as_view(), name="get_category"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
