from django.urls import path
from . import views

app_name = "blogs"

urlpatterns = [
    path("create/comment/", views.CreateComment.as_view(), name="create_comment"),
    path("<slug:slug>/", views.BlogView.as_view(), name="blog"),
]
