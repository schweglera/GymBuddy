from django import forms
from .models import Article, Workout, TrainingPlan
from .models import Comment


__FORBIDDEN_WORDS = [
    "unangemessenesWort1",
    "unangemessenesWort2",
    "unangemessenesWort3",
]


def _contains_forbidden_word(value):
    """
    Prüft, ob ein unangemessenes Wort in einem String enthalten ist.
    Args:
        value (str): Der zu prüfende String.
    Returns:
        bool: True, wenn ein unangemessenes Wort enthalten ist, sonst False.
    """
    for word in __FORBIDDEN_WORDS:
        if word.lower() in value.lower():
            return True
    return False


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]
        labels = {"title": "Titel", "content": "Inhalt"}

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")

        if title and _contains_forbidden_word(title):
            self.add_error("title", "Unangemessenes Wort im Titel gefunden.")
        if content and _contains_forbidden_word(content):
            self.add_error("content", "Unangemessenes Wort im Inhalt gefunden.")

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author", "text"]
        labels = {"author": "Autor", "text": "Text"}

    def clean(self):
        cleaned_data = super().clean()
        author = cleaned_data.get("author")
        text = cleaned_data.get("text")

        if author and _contains_forbidden_word(author):
            self.add_error("author", "Autorname enthält unangemessenes Wort.")
        if text and _contains_forbidden_word(text):
            self.add_error("text", "Unangemessenes Wort im Text gefunden.")

        return cleaned_data

# -------------------

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class WorkoutCreateForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ["date", "workout_type", "duration", "exercices"]
        labels = {"date": "Datum (YYYY-MM-DD)", "workout_type": "Trainingskategorie", "duration": "Länge", "exercices": "Übungen"}

class TrainingPlanCreateForm(forms.ModelForm):

    class Meta:
        model = TrainingPlan
        fields = ["name", "category", "exercise1", "exercise2", "exercise3", "exercise4", "exercise5", "exercise6"]
        labels = {"name": "Bezeichnung",
                  "category": "Trainingskategorie",
                  "exercise1": "Übung 1",
                  "exercise2": "Übung 2",
                  "exercise3": "Übung 3",
                  "exercise4": "Übung 4",
                  "exercise5": "Übung 5",
                  "exercise6": "Übung 6"}