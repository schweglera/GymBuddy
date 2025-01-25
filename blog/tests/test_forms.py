from django.test import TestCase
from ..forms import (
    ArticleForm,
    CommentForm,
    RegisterForm,
    AdminRegisterForm,
    WorkoutCreateForm,
    ExerciseCreateForm,
    TrainingPlanCreateForm,
    MealPlanCreateForm,
    CoachCreateForm,
)




class ArticleFormTest(TestCase):
    def test_article_form_valid_data(self):
        form = ArticleForm(data={"title": "Valider Titel", "content": "Valider Inhalt"})
        self.assertTrue(form.is_valid())

    def test_article_form_forbidden_word_in_title(self):
        form = ArticleForm(
            data={"title": "unangemessenesWort1 ist hier", "content": "Valider Inhalt"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["title"], ["Unangemessenes Wort im Titel gefunden."]
        )

    def test_article_form_forbidden_word_in_content(self):
        form = ArticleForm(
            data={"title": "Valider Titel", "content": "Hier ist unangemessenesWort2"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["content"], ["Unangemessenes Wort im Inhalt gefunden."]
        )


class CommentFormTest(TestCase):
    def test_comment_form_valid_data(self):
        form = CommentForm(data={"author": "Valider Autor", "text": "Valider Text"})
        self.assertTrue(form.is_valid())

    def test_comment_form_forbidden_word_in_author(self):
        form = CommentForm(
            data={"author": "unangemessenesWort3", "text": "Valider Text"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["author"], ["Autorname enthält unangemessenes Wort."]
        )

    def test_comment_form_forbidden_word_in_text(self):
        form = CommentForm(
            data={"author": "Valider Autor", "text": "Das ist unangemessenesWort1"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], ["Unangemessenes Wort im Text gefunden."])


class RegisterFormTest(TestCase):
    def test_register_form_valid_data(self):
        form = RegisterForm(data={
            "username": "testuser",
            "email": "test@example.com",
            "password1": "complexPass123",
            "password2": "complexPass123",
        })
        self.assertTrue(form.is_valid())

    def test_register_form_password_mismatch(self):
        form = RegisterForm(data={
            "username": "testuser",
            "email": "test@example.com",
            "password1": "complexPass123",
            "password2": "wrongPass123",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class AdminRegisterFormTest(TestCase):
    def test_admin_register_form_valid_data(self):
        form = AdminRegisterForm(data={
            "username": "adminuser",
            "password1": "complexPass123",
            "password2": "complexPass123",
            "access_code": "HWZ",
        })
        self.assertTrue(form.is_valid())

    def test_admin_register_form_invalid_access_code(self):
        form = AdminRegisterForm(data={
            "username": "adminuser",
            "password1": "complexPass123",
            "password2": "complexPass123",
            "access_code": "WRONG",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("access_code", form.errors)


class WorkoutCreateFormTest(TestCase):
    def test_workout_form_valid_data(self):
        form = WorkoutCreateForm(data={
            "date": "2025-01-25",
            "workout_type": "Ausdauer",
            "duration": "01:00:00",
        })
        self.assertTrue(form.is_valid())

    def test_workout_form_missing_fields(self):
        form = WorkoutCreateForm(data={"workout_type": "Ausdauer"})
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)
        self.assertIn("duration", form.errors)


class ExerciseCreateFormTest(TestCase):
    def test_exercise_form_valid_data(self):
        form = ExerciseCreateForm(data={
            "name": "Pushups",
            "sets": 3,
            "reps": 15,
            "weight": 0,
        })
        self.assertTrue(form.is_valid())

    def test_exercise_form_missing_fields(self):
        form = ExerciseCreateForm(data={"name": "Pushups"})
        self.assertFalse(form.is_valid())
        self.assertIn("sets", form.errors)
        self.assertIn("reps", form.errors)


class TrainingPlanCreateFormTest(TestCase):
    def test_training_plan_form_valid_data(self):
        form = TrainingPlanCreateForm(data={
            "name": "Kraft Plan",
            "category": "Kraft",
            "exercise1": "Bench Press",
            "exercise2": "Squats",
            "exercise3": "Deadlift",
            "exercise4": "",
            "exercise5": "",
            "exercise6": "",
        })
        self.assertTrue(form.is_valid())

    def test_training_plan_form_missing_name(self):
        form = TrainingPlanCreateForm(data={"category": "Kraft"})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class MealPlanCreateFormTest(TestCase):
    def test_meal_plan_form_valid_data(self):
        form = MealPlanCreateForm(data={
            "name": "Gewichtsverlustplan",
            "breakfast": "Haferflocken",
            "snack1": "Frucht",
            "lunch": "Salat mir Poulet",
            "snack2": "Nüsse",
            "dinner": "Suppe",
            "calories": 1700,
        })
        self.assertTrue(form.is_valid())


    def test_meal_plan_form_missing_fields(self):
        form = MealPlanCreateForm(data={
            "name": "Gewichtsverlustplan",
            "lunch": "",
            "dinner": "",
            "calories": None
        })

        self.assertFalse(form.is_valid())
        self.assertIn("lunch", form.errors)
        self.assertIn("dinner", form.errors)
        self.assertIn("calories", form.errors)
        self.assertNotIn("breakfast", form.errors)
        self.assertNotIn("snack1", form.errors)
        self.assertNotIn("snack2", form.errors)


class CoachCreateFormTest(TestCase):
    def test_coach_form_valid_data(self):
        form = CoachCreateForm(data={
            "name": "Max Muster",
            "category": "Fitness",
            "bio": "Zertifizierter Personal Trainer",
            "experience": 5,
            "price_hour": 50,
            "email": "max.muster@example.com",
        })
        self.assertTrue(form.is_valid())

    def test_coach_form_invalid_email(self):
        form = CoachCreateForm(data={
            "name": "Max Muster",
            "category": "Fitness",
            "bio": "Zertifizierter Personal Trainer",
            "experience": 5,
            "price_hour": 50,
            "email": "ungültige-email",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)