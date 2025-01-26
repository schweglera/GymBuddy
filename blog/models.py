from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.contrib.auth.models import User


_TITLE_MIN_LENGTH = 1
_TITLE_MAX_LENGTH = 100
_CONTENT_MIN_LENGTH = 10
_CONTENT_MAX_LENGTH = 10000
_AUTHOR_NAME_MIN_LENGTH = 2
_AUTHOR_NAME_MAX_LENGTH = 100
_COMMENT_MIN_LENGTH = 2
_COMMENT_MAX_LENGTH = 1000


class Article(models.Model):
    title = models.CharField(
        max_length=_TITLE_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                _TITLE_MIN_LENGTH,
                message=f"Titel ist zu kurz (min. {_TITLE_MIN_LENGTH} Zeichen).",
            ),
        ],
    )
    content = models.TextField(
        validators=[
            MinLengthValidator(
                _CONTENT_MIN_LENGTH,
                message=f"Inhalt ist zu kurz (min. {_CONTENT_MIN_LENGTH} Zeichen).",
            ),
            MaxLengthValidator(
                _CONTENT_MAX_LENGTH,
                message=f"Inhalt ist zu lang (max. {_CONTENT_MAX_LENGTH} Zeichen).",
            ),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.CharField(
        max_length=_AUTHOR_NAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                _AUTHOR_NAME_MIN_LENGTH,
                message=f"Autorname ist zu kurz (min. {_AUTHOR_NAME_MIN_LENGTH} Zeichen).",
            ),
        ],
    )
    text = models.TextField(
        validators=[
            MinLengthValidator(
                _COMMENT_MIN_LENGTH,
                message=f"Kommentar ist zu kurz (min. {_COMMENT_MIN_LENGTH} Zeichen).",
            ),
            MaxLengthValidator(
                _COMMENT_MAX_LENGTH,
                message=f"Kommentar ist zu lang (max. {_COMMENT_MAX_LENGTH} Zeichen)",
            ),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Kommentar von {self.author} zum Artikel '{self.article}'"

#---------------------------------------------------
import datetime


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    workout_type = models.CharField(max_length=50)
    duration = models.DurationField()

    def __str__(self):
        return f"{self.workout_type} am {self.date}"


class Exercise(models.Model): #[3]
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="exercises") #related_name macht, dass man die entsprechende Referenzierung schöner gestalten kann (default value von Django ist jeweils "name_set"
    name = models.CharField(max_length=50)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.sets}x{self.reps} @ {self.weight}kg"



class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    breakfast = models.CharField(max_length=100, blank=True, null=True)
    snack1 = models.CharField(max_length=100, blank=True, null=True)
    lunch = models.CharField(max_length=100)
    snack2 = models.CharField(max_length=100, blank=True, null=True)
    dinner = models.CharField(max_length=100)
    calories = models.IntegerField()

    def __str__(self):
        return self.name

class TrainingPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    exercise1 = models.CharField(max_length=100)
    exercise2 = models.CharField(max_length=100)
    exercise3 = models.CharField(max_length=100, blank=True, null=True)
    exercise4 = models.CharField(max_length=100, blank=True, null=True)
    exercise5 = models.CharField(max_length=100, blank=True, null=True)
    exercise6 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Coach(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    bio = models.TextField(max_length=500)
    experience = models.PositiveIntegerField()
    price_hour = models.PositiveIntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name