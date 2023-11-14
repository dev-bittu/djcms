from django.urls import path
from . import views

app_name = "manage"

urlpatterns = [
    path("blog/", views.ManageBlog.as_view(), name="blog"),
    path("category/", views.ManageCategory.as_view(), name="category"),
    path("comment/", views.ManageComment.as_view(), name="comment"),

    path("create/blog/", views.CreateBlog.as_view(), name="create_blog"),
    path("create/category/", views.CreateCategory.as_view(), name="create_category"),

    path("delete/blog/<int:id>/", views.DeleteBlog.as_view(), name="delete_blog"),
    path("delete/category/<int:id>", views.DeleteCategory.as_view(), name="delete_category"),
    path("delete/comment/<int:id>", views.DeleteComment.as_view(), name="delete_comment"),

    path("edit/blog/<int:id>/", views.EditBlog.as_view(), name="edit_blog"),
    path("edit/category/<int:id>", views.EditCategory.as_view(), name="edit_category"),
]
