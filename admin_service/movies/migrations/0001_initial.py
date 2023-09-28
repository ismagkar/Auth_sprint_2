import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FilmWork",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                ("description", models.TextField(blank=True, verbose_name="description")),
                ("creation_date", models.DateField(blank=True, null=True, verbose_name="creation date")),
                (
                    "rating",
                    models.FloatField(
                        blank=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="rating",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("movie", "movie"), ("tv_show", "tv_show")], max_length=10, verbose_name="type"
                    ),
                ),
            ],
            options={
                "verbose_name": "Кинопроизведение",
                "verbose_name_plural": "Кинопроизведения",
                "db_table": 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                ("description", models.TextField(blank=True, verbose_name="description")),
            ],
            options={
                "verbose_name": "Жанр",
                "verbose_name_plural": "Жанры",
                "db_table": 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name="GenreFilmWork",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": 'content"."genre_film_work',
            },
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("full_name", models.CharField(max_length=255, verbose_name="full name")),
            ],
            options={
                "verbose_name": "Персонал",
                "verbose_name_plural": "Персонал",
                "db_table": 'content"."person',
            },
        ),
        migrations.CreateModel(
            name="PersonFilmWork",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                (
                    "role",
                    models.CharField(
                        choices=[("actor", "actor"), ("director", "director"), ("writer", "writer")],
                        max_length=10,
                        null=True,
                        verbose_name="role",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("film_work", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="movies.filmwork")),
                ("person", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="movies.person")),
            ],
            options={
                "db_table": 'content"."person_film_work',
            },
        ),
        migrations.AddIndex(
            model_name="person",
            index=models.Index(fields=["full_name"], name="person_full_name_idx"),
        ),
        migrations.AddField(
            model_name="genrefilmwork",
            name="film_work",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="movies.filmwork"),
        ),
        migrations.AddField(
            model_name="genrefilmwork",
            name="genre",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="movies.genre"),
        ),
        migrations.AddField(
            model_name="filmwork",
            name="genres",
            field=models.ManyToManyField(through="movies.GenreFilmWork", to="movies.genre"),
        ),
        migrations.AddField(
            model_name="filmwork",
            name="persons",
            field=models.ManyToManyField(through="movies.PersonFilmWork", to="movies.person"),
        ),
        migrations.AddConstraint(
            model_name="personfilmwork",
            constraint=models.UniqueConstraint(
                fields=("film_work_id", "person_id", "role"), name="film_work_person_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="filmwork",
            index=models.Index(fields=["title"], name="film_work_title_idx"),
        ),
        migrations.AddConstraint(
            model_name="filmwork",
            constraint=models.UniqueConstraint(fields=("title", "creation_date"), name="title_creation_date_idx"),
        ),
    ]
