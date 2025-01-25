from django import forms
from .models import Article, Workout, TrainingPlan, Exercise, MealPlan, Coach
from .models import Comment
from django.forms import modelformset_factory


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

from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class AdminRegisterForm(UserCreationForm):
    access_code = forms.CharField() # [1]

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "access_code"]

    def secret_admin_code(self):
        access_code = self.cleaned_data["access_code"] # [1]
        SECRET_CODE = "HWZ"
        if access_code != SECRET_CODE:
            raise forms.ValidationError("Ungültiger Code")
        return access_code


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            admin_group, created = Group.objects.get_or_create(name="Admin")
            user.groups.add(admin_group)
        return user


class WorkoutCreateForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ["date", "workout_type", "duration"]
        labels = {"date": "Datum (yyyy-mm-dd)",
                  "workout_type": "Trainingskategorie",
                  "duration": "Länge (hh:mm:ss)"}


class ExerciseCreateForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "sets", "reps", "weight"]
        labels = {"name": "Übung",
                  "sets": "Sätze",
                  "reps": "Wiederholungen",
                  "weight": "Gewicht"}

ExerciseCreateFormSet = modelformset_factory(Exercise, form=ExerciseCreateForm, extra=1) # [3]



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


class MealPlanCreateForm(forms.ModelForm):

    class Meta:
        model = MealPlan
        fields = ["name", "breakfast", "snack1", "lunch", "snack2", "dinner", "calories"]
        labels = {"name": "Bezeichnung",
                  "breakfast": "Frühstück",
                  "snack1": "Snack 1",
                  "lunch": "Mittagessen",
                  "snack2": "Snack 2",
                  "dinner": "Abendessen",}

class CoachCreateForm(forms.ModelForm):

    class Meta:
        model = Coach
        fields = ["name","category", "bio", "experience", "price_hour", "email"]
        labels = {"name": "Name",
                  "category": "Trainingskategorie",
                  "bio": "Bio",
                  "experience": "Erfahrung in Jahren",
                  "price_hour": "Preis pro Stunde",
                  "email": "E-Mail"}
