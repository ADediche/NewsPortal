from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, CategoriesList, subscribing

urlpatterns = [
   path('', PostsList.as_view(), name = 'post_list'),
   path('<int:pk>/', PostDetail.as_view(), name = 'news_detail'),
   path('create/', PostCreate.as_view(), name = 'news_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name = 'news_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name = 'news_delete'),
   path('categories/', CategoriesList.as_view(), name = 'categories_list'),
   path('subscrib/<pk>/', subscribing, name = 'subscribing'),
]