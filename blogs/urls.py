from django.urls import path
from . import views

app_name = "blogs"

urlpatterns = [
    path("<slug:slug>/", views.BlogView.as_view(), name="blog")
]
