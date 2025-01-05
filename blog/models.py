from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

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
