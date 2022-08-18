import datetime as dt

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


def validate_year(value):
    if value > dt.datetime.now().year:
        raise ValidationError(
            'Значение года не может быть больше текущего')
    return value


class GenreCategory(models.Model):
    name = models.CharField(max_length=50,)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        abstract = True


class Genre(GenreCategory):
    """Жанры произведений."""
    class Meta:
        ordering = ['-id']
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Category(GenreCategory):
    """Категории произведение."""
    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'


class Title(models.Model):
    """Произведения."""
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(
        validators=[validate_year],
        verbose_name='Год выпуска'
    )
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        blank=True,
        null=True,
        help_text='Выберите категорию',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
        help_text='Выберите жанр'
    )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Произведения-Жанры."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre}{self.title}'


class ParentingModel(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Review(ParentingModel):
    """Отзывы."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Отзывы'
        unique_together = ('author', 'title',)


class Comment(ParentingModel):
    """Комментарии."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Комментарии'
        ordering = ['id', ]
