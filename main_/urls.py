from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main_.views import CategoriesListView, PostViewSet, CommentViewSet

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('categories/', CategoriesListView.as_view()),
    path('', include(router.urls))
]