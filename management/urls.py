from django.urls import path
from . import views

app_name = "manage"

urlpatterns = [
    path("add/blog/", views.AddBlog.as_view(), name="add_blog"),
    path("add/category/", views.AddCategory.as_view(), name="add_category"),
    path("draft/", views.DraftBlogs.as_view(), name="draft_blog"),
    path("update/", views.UpdateBlog.as_view(), name="update_blog"),
    path("edit/<int:id>/", views.EditBlog.as_view(), name="edit_blog"),
]
