from .views import (
    add_user_to_authors,
    PostDelete,
    PostDetail,
    PostEdit,
    PostsSearch,
    PostsList,
)
from django.urls import path

urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('add_user_to_authors/', add_user_to_authors, name='add_user_to_authors'),
    path('search/', PostsSearch.as_view(), name='posts_search'),
]