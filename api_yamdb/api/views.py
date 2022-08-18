from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitlesFilter
from .permissions import (IsAdminOrModeratirOrAuthor, IsAdminOrReadOnly,
                          IsAdminOrSuperUser)
from .serializers import (AuthorSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer, ReviewSerializer,
                          SignUpSerializer, TitleReadSerializer,
                          TitleWriteSerializer, TokenSerializer,
                          UserSerializer)
from .utils import generate_confirmation_code, send_confirmation_code

User = get_user_model()


class RegisterView(APIView):
    """Регистирирует пользователя и отправляет ему код подтверждения."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid()
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        if serializer.is_valid():
            confirmation_code = generate_confirmation_code()
            user = User.objects.filter(email=email).exists()
            if not user:
                User.objects.create_user(email=email, username=username)
                User.objects.filter(email=email).update(
                    confirmation_code=generate_confirmation_code())
                send_confirmation_code(email, confirmation_code)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                'Такой пользователь уже зарегистирован',
                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    """Проверяет код подтверждения и отправляет токен."""
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(
            User,
            username=username,
        )
        if user.confirmation_code != confirmation_code:
            return Response(
                'Confirmation code is invalid',
                status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response(
            {'access_token': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """Админ получает список пользователей или создает нового"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperUser, ]
    lookup_field = 'username'
    search_fields = ('username', )


class MeView(APIView):
    """Пользователь может посмотреть свой профиль и изменить его"""

    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(
            'Вы не авторизованы',
            status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            if request.user.role == 'admin':
                serializer = UserSerializer(
                    user,
                    data=request.data,
                    partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = AuthorSerializer(
                    user,
                    data=request.data,
                    partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return Response(
            'Вы не авторизованы',
            status=status.HTTP_401_UNAUTHORIZED)


class CLDMixinSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class GenreViewSet(CLDMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'


class CategoryViewSet(CLDMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    search_fields = ('=name',)
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrModeratirOrAuthor]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    serializer_class = ReviewSerializer

    def title_query(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.title_query().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title_query())


class CommentViewSet(ReviewViewSet):
    serializer_class = CommentSerializer

    def review_query(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return Comment.objects.filter(review=self.review_query().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review_query())
