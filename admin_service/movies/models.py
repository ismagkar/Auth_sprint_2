import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content"."genre'
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full name"), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content"."person'
        verbose_name = "Персонал"
        verbose_name_plural = "Персонал"

        indexes = [
            models.Index(fields=["full_name"], name="person_full_name_idx"),
        ]


class FilmWork(UUIDMixin, TimeStampedMixin):
    class FilmType(models.TextChoices):
        MOVIE = "movie", _("movie")
        TV_SHOW = "tv_show", _("tv_show")

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    creation_date = models.DateField(_("creation date"), blank=True, null=True)
    rating = models.FloatField(_("rating"), blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.CharField(_("type"), max_length=10, choices=FilmType.choices)
    genres = models.ManyToManyField(Genre, through="GenreFilmWork")
    persons = models.ManyToManyField(Person, through="PersonFilmWork")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = "Кинопроизведение"
        verbose_name_plural = "Кинопроизведения"

        indexes = [
            models.Index(fields=["title"], name="film_work_title_idx"),
        ]
        constraints = [models.UniqueConstraint(fields=["title", "creation_date"], name="title_creation_date_idx")]


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.film_work} - {self.genre}"

    class Meta:
        db_table = 'content"."genre_film_work'


class PersonFilmWork(UUIDMixin):
    class RoleType(models.TextChoices):
        ACTOR = "actor", _("actor")
        DIRECTOR = "director", _("director")
        WRITER = "writer", _("writer")

    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(_("role"), null=True, max_length=10, choices=RoleType.choices)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.film_work} - {self.person}"

    class Meta:
        db_table = 'content"."person_film_work'

        constraints = [
            models.UniqueConstraint(fields=["film_work_id", "person_id", "role"], name="film_work_person_idx")
        ]
