from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet, MeView,
                    RegisterView, ReviewViewSet, TitleViewSet, TokenView,
                    UserViewSet)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename='comments'
)

urlpatterns_auth = [
    path('signup/', RegisterView.as_view()),
    path('token/', TokenView.as_view())
]

urlpatterns = [
    path('v1/auth/', include(urlpatterns_auth)),
    path('v1/users/me/', MeView.as_view()),
    path('v1/', include(router_v1.urls)),
]
