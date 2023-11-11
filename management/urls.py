from django.urls import path
from . import views

app_name = "manage"

urlpatterns = [
    path("add/", views.AddBlog.as_view(), name="add_blog")
]
