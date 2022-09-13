from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path('',views.BoardIndexView.as_view(),name='home'),
    path('create/', views.BoardCreateView.as_view(), name='create'),
    path("<str:boardName>/",views.BoardListView.as_view(),name='aboard'),
    path('<str:boardName>/search/',views.BoardSearchView.as_view(),name='search'),
    path("<str:boardName>/post/",views.BoardPostView.as_view(),name="post"),
    path("<str:boardName>/<int:postID>/",views.PostDetailView.as_view(),name="detail"),
    path("<str:boardName>/<int:postID>/edit/",views.PostUpdateView.as_view(),name="update"),
    path("<str:boardName>/<int:postID>/delete/",views.PostDeleteView.as_view(),name="delete"),
    path("<str:boardName>/<int:postID>/<int:commentID>/delete/",views.CommentDeleteView.as_view(),name="CDelete"),
    path("<str:boardName>/<int:postID>/<int:commentID>/edit/",views.CommentUpdateView.as_view(),name="CEdit"),
    path("<int:postID>/like/",views.PostLikeView.as_view(),name="like"),
    path("<str:boardName>/recommend/",views.PostLikeSearchView.as_view(),name="likeSearch"),
]