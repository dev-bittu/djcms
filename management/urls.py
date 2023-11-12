from django.urls import path
from . import views

app_name = "manage"

urlpatterns = [
    path("add/blog/", views.AddBlog.as_view(), name="add_blog"),
    path("add/category/", views.AddCategory.as_view(), name="add_category"),
    path("draft/", views.DraftBlogs.as_view(), name="draft_blog"),
    path("update/", views.UpdateBlog.as_view(), name="update_blog"),
    path("delete/", views.DeleteBlogs.as_view(), name="delete_blog"),
    path("delete/<int:id>/", views.DeleteBlog.as_view(), name="delete"),
    path("edit/<int:id>/", views.EditBlog.as_view(), name="edit_blog"),
]
